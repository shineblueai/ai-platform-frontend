from student_exam import student_exam_ui
import streamlit as st
from auth import login
from student_dashboard import student_ui
from company_dashboard import company_ui
from admin_dashboard import admin_ui

st.set_page_config(page_title="AI Hiring Platform", layout="wide")

st.markdown("""<h1 style='text-align: center; color: #4CAF50;'>🌟 AI Hiring & Learning Platform 🌟</h1>""", unsafe_allow_html=True)

role = st.sidebar.selectbox("Login as:", ["Student", "Company", "Admin"])
email, token = login(role)

if token:
    st.success("Login successful!")
    if role == "Student":
        tab = st.sidebar.radio("Select Option", ["Dashboard", "Take Exam"])
    if tab == "Dashboard":
        student_ui(email, token)
    elif tab == "Take Exam":
        student_exam_ui(email, token)
    elif role == "Company":
        company_ui(email, token)
    elif role == "Admin":
        admin_ui(email, token)