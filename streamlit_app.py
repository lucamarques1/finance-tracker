import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os

log_in_page = st.Page("streamlit_app.py", title = "Log-In", icon="⚙️")
insert_transaction_page = st.Page("insert_trans.py", title="Insert Transaction", icon="💸")

pg = st.navigation([log_in_page,insert_transaction_page])
pg.run()

st.set_page_config(
    page_title="PerFin Log In",
    page_icon="💰",
    page_name = "Log In"
)
supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]

url: str = supabase_url
key: str = supabase_key
supabase: Client = create_client(url, key)





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
            st.switch_page("pages/insert_trans.py")
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    if st.button("Sign Up"):
        try:
            supabase.auth.sign_up({"email": email, "password":password})
            st.info("Account created! Check your email for verification.")
        except Exception as e:
            st.error(f"Error {e}")
