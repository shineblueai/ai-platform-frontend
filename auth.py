import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def login(role):
    st.sidebar.subheader(f"{role} Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    token = None

    if st.sidebar.button("Login"):
        res = requests.post(f"{BACKEND_URL}/user/login", json={
            "email": email,
            "password": password
        })
        if res.status_code == 200:
            token = res.json()["access_token"]
        else:
            st.sidebar.error("Login failed.")
    return email, token