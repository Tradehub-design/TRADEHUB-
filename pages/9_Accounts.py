import streamlit as st
from utils.supabase_client import get_supabase_client

st.title("🏦 Accounts")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

st.subheader("Add MT5 Account")

with st.form("add_account"):
    account_number = st.text_input("Account Number")
    account_name = st.text_input("Account Name")
    broker = st.text_input("Broker", value="Fusion Markets")
    platform = st.text_input("Platform", value="MT5")
    account_type = st.selectbox(
        "Account Type",
        ["Live", "Demo", "Challenge", "Funded", "Prop Firm"]
    )
    currency = st.selectbox("Currency", ["AUD", "USD", "GBP", "EUR"])
    starting_balance = st.number_input("Starting Balance", min_value=0.0)

    submitted = st.form_submit_button("Add Account")

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
                "current_balance": starting_balance
            }).execute()

            st.success("Account added successfully.")

st.divider()

st.subheader("Existing Accounts")

response = supabase.table("accounts").select("*").execute()
accounts = response.data

if accounts:
    st.dataframe(accounts, use_container_width=True)
else:
    st.info("No accounts added yet.")
