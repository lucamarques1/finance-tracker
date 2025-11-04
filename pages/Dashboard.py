import streamlit as st
from supabase import create_client, Client


st.set_page_config(
    page_title="Hello!",
    page_icon="👋"
)

st.title("Welcome to your Dashboard")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in first!")
    st.stop()


with st.form("New Transaction"):
    st.write("Record your new Transaction")
    st.text_input("What is the subject?")
    