import streamlit as st
from langchain.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import os
import pandas as pd
import chromadb
import uuid
import re

# Load environment variables
load_dotenv()

# Utility function for cleaning text
def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

# Portfolio class for handling job skills and links
class Portfolio:
    def __init__(self, file_path="./resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

# Chain class for processing job data and generating emails
class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing
            the following keys: `role`, `experience`, `skills`, and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE)
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context is too big. Unable to extract job postings.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Sri Sai Srivatsa Yerrapragada, a recent graduate with a Master's degree in Electrical and Computer Engineering, specializing in Machine Learning, with a minor in Computer Science at the University of Florida.
            With one year of industry experience as a Software Developer at Accenture, you have developed a profound interest in Machine Learning and software engineering, demonstrating proficiency in multiple programming languages and databases. 
            Furthermore, you have earned industry-recognized certifications, including the AWS Certified Developer, AWS Solution Architect Associate, and AWS Machine Learning Specialty.

            Your job is to write a cold email to the client regarding the job mentioned above, describing Sri Sai Srivatsa Yerrapragada's capability in fulfilling their needs.

            Also, add the most relevant ones from the following links to showcase Srivatsa's portfolio: {link_list}.
            Remember, you are Sri Sai Srivatsa Yerrapragada. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

# Streamlit app creation
def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Email Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.apple.com/en-us/details/200565688/aiml-machine-learning-platform-infrastructure?team=SFTWR")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            loaded_data = loader.load()
            if not loaded_data:
                st.error("Unable to load data from the provided URL.")
                return

            data = clean_text(loaded_data.pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            for job in jobs:
                skills = job.get('skills', [])
                if not skills:
                    st.warning("No skills found to query.")
                    continue
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

# Main entry point
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Email Generator")
    create_streamlit_app(chain, portfolio, clean_text)
