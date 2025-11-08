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
time_filter = st.sidebar.radio("Apply Time Filters", ["No", "Yes"])
select_month = st.sidebar.selectbox("Month", range(1,13))
select_year = st.sidebar.number_input("Year", min_value= 2023, max_value=3000)

# Select Category
category_filter = st.sidebar.radio("Apply Category Filters", ["No", "Yes"])
select_category = st.sidebar.selectbox("Category", ["All", "Food", "Rent", "Transport", "Entertainment", "Shopping", "Health", "Savings", "Other"])


# Apply Filters

## Flow Type
query = supabase.table("transactions").select("*").eq("user_id", user_id)
if flow_type == "Income": 
    query = query.gt("amount", 0)
elif flow_type == "Expense":
    query = query.lt("amount", 0)

## Category
if category_filter == "Yes":
    if select_category != "All": 
        query = query.eq("category", select_category)

## Date
if time_filter == "Yes":
    start_date = date(select_year, select_month, 1)
    if select_month == 12:
        end_date = date(select_year + 1, 1, 1)
    else: 
        end_date = date(select_year, select_month + 1, 1)

    query = query.gte("date", str(start_date)).lt("date", str(end_date))


## Short Cut Buttons
today = date.today()

if all_time:
    # No filter
    pass
elif this_year:
    button_start = date(today.year, 1, 1)
    button_end = date(today.year + 1, 1, 1)
    query = query.gte("date", str(button_start)).lt("date", str(button_end))
elif this_month:
    button_start = date(today.year, today.month, 1)
    if today.month == 12:
        button_end = date(today.year + 1, 1, 1)
    else:
        button_end = date(today.year, today.month + 1, 1)
    query = query.gte("date", str(button_start)).lt("date", str(button_end))
elif this_week:
    button_start = today - timedelta(days=today.weekday())
    button_end = button_start + timedelta(days=7)
    query = query.gte("date", str(button_start)).lt("date", str(button_end))


response = query.execute()
data = pd.DataFrame(response.data)

# KPIs

total_income = data.loc[data["amount"] > 0, "amount"].sum()
total_expense = data.loc[data["amount"] < 0, "amount"].sum()
net_profit = total_income + total_expense

savings_rate = float(data.loc[data["category"] == "Savings", "amount"].sum() /  - total_expense) * 100


st.header("KPIs")
st.info(f"Total Income: {total_income}")
st.info(f"Total Expense: {total_expense}")
st.info(f"Net Profit: {net_profit}")
st.info(f"Savings Rate: {savings_rate}%")
