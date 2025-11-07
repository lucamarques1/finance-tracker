import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Password Reset Page"
)

st.title("🔑 Reset Your Password")
new_password = st.text_input("Please enter your new password", type = "password")
new_password_confirmation = st.text_input("Please confirm your new password", type = "password")
confirm = st.button("Confirm")

if confirm:
    if new_password == new_password_confirmation:
        try:
            supabase.auth.update_user({'password': new_password})
        except Exception as e:
            st.error(f"Error {e}")
    else: 
        st.warning("The passwords don't match!")


