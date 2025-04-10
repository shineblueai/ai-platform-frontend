import streamlit as st
import requests
import os
import base64
from datetime import datetime

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def student_exam_ui(email, token):
    st.header("🧪 Take Your Exam")

    headers = {"token": token}

    # Capture webcam photo
    st.subheader("📸 Capture Your Photo Before Starting")
    img = st.camera_input("Take a photo before you begin")

    # Fetch available exams
    st.subheader("📋 Available Exams")
    response = requests.get(f"{BACKEND_URL}/exam/list", headers=headers)
    if response.status_code != 200:
        st.error("No exams available or access denied.")
        return

    exams = response.json()
    if not exams:
        st.info("No exams currently assigned.")
        return

    selected_exam = st.selectbox("Choose an exam to start:", [e["title"] for e in exams])
    exam_data = next((e for e in exams if e["title"] == selected_exam), None)

    if exam_data:
        answers = {}
        st.subheader("📝 Answer the following questions:")

        for i, q in enumerate(exam_data["questions"]):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            answers[i] = st.radio(f"Your answer:", q["options"], key=f"q{i}")

        if st.button("Submit Exam"):
            result = {
                "email": email,
                "exam_id": str(exam_data["_id"]),
                "answers": answers,
                "photo": base64.b64encode(img.getvalue()).decode() if img else None,
                "submitted_at": str(datetime.now())
            }
            submit_res = requests.post(f"{BACKEND_URL}/exam/submit", json=result, headers=headers)
            if submit_res.status_code == 200:
                st.success("Exam submitted successfully!")
                st.json(submit_res.json())
            else:
                st.error("Submission failed.")