import streamlit as st
from langchain.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


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


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Email Generator")
    create_streamlit_app(chain, portfolio, clean_text)
