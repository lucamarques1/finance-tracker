import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
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



if data.empty:
    st.warning("No transactions found for selected filters")
    st.stop()

st.header("KPIs")
st.info(f"Total Income: € {total_income:,.2f}")
st.info(f"Total Expense: € {total_expense:,.2f}")
st.info(f"Net Profit: € {net_profit:,.2f}")
st.info(f"Savings Rate: {savings_rate} %")

data.columns = [c.lower().strip() for c in data.columns]
data["amount"] = pd.to_numeric(data["amount"], errors="coerce").fillna(0)
data["date"] = pd.to_datetime(data["date"], errors="coerce")

# First Table "DATA PREVIEW":
wanted = ["date", "description", "category", "amount"]
cols = [c for c in wanted if c in data.columns]

view = ( 
    data.loc[:, cols]
    .assign(date=lambda df: pd.to_datetime(df["date"], errors="coerce").dt.date)
    .sort_values("date", ascending=False)
)
st.dataframe(
    view,
    hide_index=True,
    column_config={
        "amount": st.column_config.NumberColumn("Amount (€)", format = "€ %.2f"),
        "date": st.column_config.DateColumn("Date"),
        "category": st.column_config.TextColumn("Category"),
        "description": st.column_config.TextColumn("Description"),
    },

)

st.write(data.dtypes)
st.write("Number of Transactions:", len(data))

#Income vs Expense over time
data["month"] = data["date"].dt.to_period("M").astype(str)
data["type"] = np.where(data["amount"] > 0, "Income", "Expense")
monthly_summary = data.groupby(["month", "type"])["amount"].sum().reset_index()
fig = px.bar(
    monthly_summary, 
    x="month",
    y="amount",
    color="type",
    barmode="group",
    title="Monthly Income vs. Expenses",
    text_auto=".2s"
)
st.plotly_chart(fig, use_container_width=True)

# Pie Chart for Categories
expense_data = data[data["amount"]<0]
category_summary = (
    expense_data.groupby("category")["amount"]
    .sum()
    .abs()
    .reset_index()
)

fig2 = px.pie(
    category_summary,
    names="category",
    values="amount",
    title="📊 Expense Breakdown by Category"
)
st.plotly_chart(fig2, use_container_width=True)

# Cumulative Net Worth Over time
data = data.sort_values("date")
data["cumulative_net"] = data["amount"].cumsum()

fig3 = px.line(
    data,
    x="date",
    y="cumulative_net",
    title="📈 Cumulative Net Worth Over Time"
)
st.plotly_chart(fig3, use_container_width=True)


# Spending by Weekday
data["weekday"] = data["date"].dt.day_name()

weekday_expenses = (
    data[data["amount"] < 0]
    .groupby("weekday")["amount"]
    .sum()
    .abs()
    .reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    .reset_index()
)

fig4 = px.bar(
    weekday_expenses,
    x="weekday",
    y="amount",
    title="🗓 Spending by Weekday",
    text_auto=".2s"
)
st.plotly_chart(fig4, use_container_width=True)

#Savings Rate 
monthly_savings = (
    monthly_summary
    .pivot(index="month", columns="type", values="amount")
    .fillna(0)
    .reset_index()
)

monthly_savings["savings_rate"] = (
    monthly_savings["Income"] + monthly_savings["Expense"]
) / monthly_savings["Income"] * 100

fig5 = px.line(
    monthly_savings,
    x="month",
    y="savings_rate",
    title="💾 Monthly Savings Rate Trend (%)"
)
st.plotly_chart(fig5, use_container_width=True)

#Income Category Projection
income_data = data[data["amount"] > 0]
income_summary = income_data.groupby("category")["amount"].sum().reset_index()

fig6 = px.pie(
    income_summary,
    names="category",
    values="amount",
    title="💰 Income Breakdown by Category"
)
st.plotly_chart(fig6, use_container_width=True)