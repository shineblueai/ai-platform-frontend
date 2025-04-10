import streamlit as st
import requests
import os
import json

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def company_ui(email, token):
    st.header("🏢 Company Dashboard")

    title = st.text_input("Exam Title")
    description = st.text_input("Exam Description")
    tech_stack = st.text_input("Tech Stack")

    questions_input = st.text_area("Questions (JSON format)", height=200,
        help='Example: [{"question": "What is Python?", "options": ["Lang", "Car"], "answer": "Lang"}]')

    if st.button("Create Exam"):
        try:
            questions = json.loads(questions_input)
            headers = {"token": token}
            res = requests.post(f"{BACKEND_URL}/exam/create", json={
                "title": title,
                "description": description,
                "tech_stack": tech_stack,
                "questions": questions
            }, headers=headers)
            if res.status_code == 200:
                st.success("Exam created successfully!")
            else:
                st.error("Failed to create exam.")
        except Exception as e:
            st.error(f"Invalid question format: {e}")