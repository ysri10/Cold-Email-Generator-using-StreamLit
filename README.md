# Email Generator for Job Postings  

## Overview  
This project is an **automated email generation system** that scrapes job postings from URLs, extracts relevant job descriptions, and generates personalized emails. The application utilizes **Streamlit** for the frontend interface and **LangChain** for language processing. The email generation is powered by **LLaMA 3.1-70B** through **GroqCloud** to provide dynamic, context-aware email content.  

## Key Features  
- **Job Scraping** – Extracts job postings directly from web pages using URLs.  
- **Dynamic Email Generation** – Personalized cold emails are generated based on extracted job descriptions and the user’s portfolio.  
- **Portfolio Integration** – Queries relevant links and projects from the user’s portfolio to enrich the generated emails.  
- **Streamlit Interface** – Simple and interactive frontend for entering URLs and triggering email generation.  
- **LLM Integration** – Powered by LLaMA 3.1-70B via GroqCloud, ensuring high-quality language output.  

## How It Works  
1. **User Input** – Users provide a URL linking to job postings (e.g., Apple Careers).  
2. **Web Scraping** – The application scrapes the job data from the provided URL.  
3. **Job Extraction** – LangChain extracts job postings and relevant details (role, skills, experience).  
4. **Portfolio Querying** – Extracted skills are matched with projects in the user’s portfolio using **Chromadb**.  
5. **Email Generation** – A personalized email is generated showcasing relevant projects and skills.  

## Project Architecture  
- **Frontend** – Built with **Streamlit** to provide a user-friendly interface for URL submission and displaying email output.  
- **Backend** – Developed in Python using **LangChain** to handle job extraction and email generation.  
- **Database** – Portfolio data is managed through **Chromadb** to enable querying of skills and project links.  

## Technologies and Tools  
- **LangChain**  
- **Streamlit**  
- **LLaMA 3.1-70B (GroqCloud)**  
- **Chromadb**  
- **Python**  
- **Pandas**  
- **WebBaseLoader**  

## Installation and Setup  

### Prerequisites  
- **Python 3.8+**  
- **pip**  
- **Streamlit**  
- **Chromadb**  
- **LangChain**  

### Setup  
1. Clone the repository:  
   ```bash  
   git clone <repo-link>  
   cd project-directory  
   ```  

2. Install required packages:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Set up environment variables:  
   ```bash  
   cp .env.example .env  
   ```  
   - Add your **GROQ_API_KEY** to the `.env` file.  

4. Run the application:  
   ```bash  
   streamlit run app.py  
   ```  

## File Structure  
- **app.py** – Main Streamlit application handling user input and email generation.  
- **chains.py** – Defines the Chain class for extracting job postings and generating emails.  
- **main.py** – Core logic for text cleaning, portfolio handling, and job extraction.  
- **portfolio.py** – Manages portfolio data and performs skill-based queries using Chromadb.  
- **utils.py** – Utility functions for cleaning extracted job text.  

## Usage  
1. Launch the application.  
2. Enter a URL with job postings.  
3. Submit the URL and view the generated personalized email.  
4. Copy or modify the email as needed for outreach.  

## Future Enhancements  
- **Multi-URL Input** – Allow users to input multiple URLs at once.  
- **Enhanced Email Templates** – Support for multiple email templates for different job categories.  
- **Portfolio Expansion** – Integrate more data sources to enrich the user portfolio for querying.  
