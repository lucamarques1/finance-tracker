import streamlit as st
import pandas as pd
import matplotlib as plt
from supabase import create_client, Client

# Connect to supabase securely
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)


st.title("💹 PerFin Dashboard")
st.write(
    "This is your personal finance tracker with integrated AI recommendations."
)

uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
st.sidebar.info("Upload a CSV with columns: date, description, amount, category.")

       
