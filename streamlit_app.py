import streamlit as st
import pandas as pd
from supabase import create_client, Client

st.set_page_config(
    page_title="PerFin Log In",
    page_icon="💰"
)

# Connect to supabase securely
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]

if "access_token" in st.session_state:
    supabase =create_client(url, st.session_state.access_token)
else:
    supabase = create_client(url, key)  # fallback (not recommended)

# Title
st.title(" PerFin Dashboard")
st.write(
    "Please log in with your Account to see your data."
)


#INIT SUPABASE
if "user" not in st.session_state:
    st.session_state.user = None

email = st.text_input("Email", key="login_email")
password = st.text_input("Password", type = "password", key="login_password")

col1, col2 = st.columns(2)
with col1: 
    if st.button("Sign In"):
        try: 
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = res.user
            st.session_state.access_token = res.session.access_token
            st.success("✅ Logged in successfully!")
            st.write(f"Access Token: {st.session_state.access_token}")
            st.switch_page("pages/dashboard.py")
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    if st.button("Sign Up"):
        try:
            supabase.auth.sign_up({"email": email, "password":password})
            st.info("Account created! Check your email for verification.")
        except Exception as e:
            st.error(f"Error {e}")
