import streamlit as st
from supabase import create_client, Client


st.title("Welcome to your Dashboard")

# --- SUPABASE SETUP ---
url: str = st.secrets["supabase"]["url"]
key: str = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)


if "access_token" in st.session_state:
    supabase.postgrest.auth(st.session_state.access_token)
else:
    st.warning("Please log in first.")
    st.stop()


user = st.session_state.user
user_id = user.id


categories = ["Food", "Rent", "Transport", "Entertainment", "Shopping", "Health", "Savings", "Other"]
with st.form("New Transaction"):
    st.write("Record your new Transaction")
    subject = st.text_input("What is the subject of the transaction?")
    category = st.selectbox("Category", categories)
    amount = st.number_input("What's the amount?")
    date = st.date_input("What's the date of the transaction?")
    description = st.text_input("Description (optional)")
    submitted = st.form_submit_button("Submit the new transaction!")

    if submitted: 
        data = {
            "user_id": st.session_state.user.id,
            "date": str(date),
            "category": category,
            "amount": amount,
            "description": description
        }


        try: 
            supabase.table("transactions").insert(data).execute()
        except Exception as e:
            st.error(f"Error adding transaction: {e}")