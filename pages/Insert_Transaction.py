import streamlit as st
from supabase import create_client, Client


st.title("💸 Insert a New Cash Flow")

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
    amount = 0 - float(st.number_input("What's the amount?"))
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


with st.form("New Income"):
    st.write("Record new Cash In-flow")
    subject_2 = st.text_input("What's the Title of the Income")
    category_2 = st.selectbox("Category", ["Parental Help", "Work", "Business"])
    amount_2 = st.number_input("Amount")
    date_2 = st.date_input("Date of the Income")
    description_2 = st.text_input("Description (optional)")
    submitted_2 = st.form_submit_button("Submit new Income")

    if submitted_2:
        data_2 = {
            "user_id": st.session_state.user.id,
            "date": str(date_2),
            "category": category_2,
            "amount": amount_2,
            "description": description_2
        }

        try:
            supabase.table("transactions").insert(data_2).execute()
        except Exception as e:
            st.error(f"Error adding Income: {e}")