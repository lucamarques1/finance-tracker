import streamlit as st
import numpy as np
import pandas as pd
import matplotlib as plt
from supabase import Client, create_client 
from datetime import date, datetime, timedelta

# --- SUPABASE SETUP ---
url: str = st.secrets["supabase"]["url"]
key: str = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)


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

user_id = st.session_state.user.id

st.info("Welcome back!")

st.sidebar.title("Filters")

#Filter for Income or Expense
flow_type = st.sidebar.radio("Flow Type", ["All", "Income", "Expense"])
# Filter for Time now
col1,col2,col3,col4 = st.columns(4)

with col1:
    all_time = st.button("All time")
with col2:
    this_year = st.button("This Year")
with col3:
    this_month = st.button("This Month")
with col4:
    this_week = st.button("This Week")




# Select Month and Year
select_month = st.sidebar.selectbox("Month", range(1,13))
select_year = st.sidebar.number_input("Year", min_value= 2023, max_value=3000)

# Select Category
select_category = st.sidebar.selectbox("Category", ["All", "Food", "Rent", "Transport", "Entertainment", "Shopping", "Health", "Savings", "Other"])


# Apply Filters
## Flow Type
query = supabase.table("transactions").select("*").eq("user_id", user_id)
if flow_type == "Income": 
    query = query.gt("amount", 0)
elif flow_type == "Expense":
    query = query.lt("amount", 0)

## Category
if select_category != "All": 
    query = query.eq("category", select_category)

## Date
start_date = date(select_year, select_month, 1)
if select_month == 12:
    end_date = date(select_year + 1, 1, 1)
else: 
    end_date = date(select_year, select_month + 1, 1)

## Short Cut Buttons
if all_time:
    query = query 
elif this_year:
    this_year_start = str(date.today()).split("-")[0]
    this_year_end = this_year_start + 1
elif this_month:
    this_month_start = str(date.today()).split("-")[1]
elif this_week:
    start_of_week = date.today() - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
