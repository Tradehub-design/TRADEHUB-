import streamlit as st
from utils.supabase_client import get_supabase_client

st.title("🏦 Accounts")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

st.subheader("Add / Update Account")

with st.form("account_form"):
    account_number = st.text_input("MT5 Account Number")
    account_name = st.text_input("Account Name")
    broker = st.text_input("Broker", value="Fusion Markets")
    platform = st.text_input("Platform", value="MT5")
    account_type = st.selectbox(
        "Account Type",
        ["Live", "Demo", "Challenge", "Funded", "Prop Firm"]
    )
    currency = st.selectbox("Currency", ["AUD", "USD", "GBP", "EUR"])
    starting_balance = st.number_input("Starting Balance", min_value=0.0)
    current_balance = st.number_input("Current Balance", min_value=0.0)

    submitted = st.form_submit_button("Save Account")

    if submitted:
        if not account_number:
            st.error("Account number is required.")
        else:
            supabase.table("accounts").upsert({
                "account_number": account_number,
                "account_name": account_name,
                "broker": broker,
                "platform": platform,
                "account_type": account_type,
                "currency": currency,
                "starting_balance": starting_balance,
                "current_balance": current_balance
            }).execute()

            st.success("Account saved.")

st.divider()

st.subheader("Existing Accounts")

response = supabase.table("accounts").select("*").execute()
accounts = response.data

if accounts:
    st.dataframe(accounts, use_container_width=True)
else:
    st.info("No accounts added yet.")
