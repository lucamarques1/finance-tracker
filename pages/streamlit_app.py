import streamlit as st
import pandas as pd
import matplotlib as plt
from supabase import create_client, Client

# Connect to supabase securely
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

# Title
st.title("💹 PerFin Dashboard")
st.write(
    "Please log in with your Account to see your data."
)


# Log In Screen
email = st.text_input("Email")
password = st.text_input("Password")

if st.button("Sign In"):
    st.session_state.user = user
    st.success("Logged In")
else:
    st.error("Invalid Credentials")

if st.button("Sign Up"):
    supabase.auth.sign_up({"email": email, "password": password})
    st.success("Account created. Please log in")
