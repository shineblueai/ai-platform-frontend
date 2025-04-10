import pdfplumber
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def analyze_resume_with_jd(resume_text: str, job_description: str):
    prompt = f"""
You are an AI hiring assistant. A candidate has submitted their resume. Evaluate the resume based on the given job description.

Resume:
{resume_text}

Job Description:
{job_description}

Please provide:
1. Match score out of 100
2. Matched skills
3. Missing skills
4. Resume improvement suggestions
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an intelligent resume screening assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content