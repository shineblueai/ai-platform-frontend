import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def student_ui(email, token):
    st.header("🎓 Student Dashboard")
    tab1, tab2 = st.tabs(["Analyze Resume", "Past Reports"])

    with tab1:
        jd = st.text_area("Paste the Job Description")
        uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

        if st.button("Analyze Resume"):
            if uploaded_file and jd:
                files = {"resume": uploaded_file}
                data = {"job_description": jd}
                headers = {"token": token}
                res = requests.post(f"{BACKEND_URL}/resume/analyze/save", files=files, data=data, headers=headers)
                if res.status_code == 200:
                    st.success("Resume analyzed and saved!")
                    st.text_area("Analysis Result", res.json()["analysis"], height=300)
                else:
                    st.error("Error during analysis.")

        if st.button("Download PDF Report"):
            if uploaded_file and jd:
                files = {"resume": uploaded_file}
                data = {"job_description": jd}
                headers = {"token": token}
                res = requests.post(f"{BACKEND_URL}/resume/analyze/pdf", files=files, data=data, headers=headers)
                if res.status_code == 200:
                    with open("report.pdf", "wb") as f:
                        f.write(res.content)
                    with open("report.pdf", "rb") as f:
                        st.download_button(label="Download Report", data=f, file_name="resume_analysis.pdf")
                else:
                    st.error("Could not generate PDF.")

    with tab2:
        headers = {"token": token}
        res = requests.get(f"{BACKEND_URL}/resume/history", headers=headers)
        if res.status_code == 200:
            reports = res.json()
            for r in reports:
                st.markdown("---")
                st.write(f"📅 {r['timestamp']} | 📄 JD: {r['job_description'][:80]}...")
                st.text_area("🔍 Analysis", r['analysis'], height=200)
        else:
            st.error("Unable to fetch past reports.")