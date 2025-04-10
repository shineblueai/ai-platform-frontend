import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def admin_ui(email, token):
    st.header("🛡️ Admin Dashboard")
    headers = {"token": token}

    st.subheader("Registered Users")
    try:
        res = requests.get(f"{BACKEND_URL}/admin/users", headers=headers)
        if res.status_code == 200:
            users = res.json()
            for user in users:
                st.write(user)
        else:
            st.error("Unable to fetch users.")
    except:
        st.error("Server connection error.")