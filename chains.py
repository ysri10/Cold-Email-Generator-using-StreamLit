import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

os.getenv("GROQ_API_KEY")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
                     temperature = 0,
                        groq_api_key=os.getenv("GROQ_API_KEY"),
                        model_name = "llama-3.1-70b-versatile"
                    )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return the, in JSON format containing
            following keys: `role`, `experience`, `skills` and `description`.
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

    def write_mail(self,job,links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Sri Sai Srivatsa Yerrapragada, I am recently graduated in Master's degree in Electrical and Computer Engineering, specializing in Machine Learning, with a minor in Computer Science at the University of Florida.
            With one year of industry experience as a Software Developer at Accenture, I have developed a profound interest in Machine Learnning and software engineering, demonstrating proficiency in multiple programming languages and databases. 
            Furthermore, I have earned industry-recognized certifications, including the AWS Certified Developer, AWS Solution Architect Associate and AWS Machine Learning Speciality. 

            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Sri Sai Srivatsa Yerrapragada 
            in fulfilling their needs.

            Also add the most relevant ones from the following links to showcase Srivatsa's portfolio: {link_list}
            Remember you are Sri Sai Srivatsa Yerrapragada. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
