import streamlit as st
from supabase import create_client, Client


st.set_page_config(
    page_title="Hello!"
    page_icon="👋"
)

st.write(" # Welcome to the PerFin Dashboard!")

st.sidebar.sucess("Select a page above")
st.sidebar.selectbox
