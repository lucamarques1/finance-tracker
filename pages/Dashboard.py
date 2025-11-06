import streamlit as st
import numpy as np
import pandas as pd
import supabase as sp

st.set_page_config(
    page_title="PerFin Dashboard",
    page_icon="📊"
)
st.title("📊 PerFin Dashbaord")

if "access_token" in st.session_state:
    supabase.postgrest.auth(st.session_state.access_token)
else:
    st.warning("Please log in first.")
    st.stop()

st.info("Welcome back!")

