import streamlit as st
from utils.supabase_client import get_supabase_client

st.title("⚙️ Settings")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

st.subheader("Add / Update Funded Rules")

accounts_response = supabase.table("accounts").select("*").execute()
accounts = accounts_response.data

if not accounts:
    st.info("Add an account first in the Accounts page.")
    st.stop()

account_options = [a["account_number"] for a in accounts]

with st.form("funded_rules_form"):
    account_number = st.selectbox("Account", account_options)
    starting_balance = st.number_input("Starting Balance", min_value=0.0)
    max_daily_loss = st.number_input("Max Daily Loss", min_value=0.0)
    max_total_loss = st.number_input("Max Total Loss", min_value=0.0)
    profit_target = st.number_input("Profit Target", min_value=0.0)
    min_trading_days = st.number_input("Minimum Trading Days", min_value=0, step=1)

    submitted = st.form_submit_button("Save Rules")

    if submitted:
        supabase.table("funded_rules").upsert({
            "account_number": account_number,
            "starting_balance": starting_balance,
            "max_daily_loss": max_daily_loss,
            "max_total_loss": max_total_loss,
            "profit_target": profit_target,
            "min_trading_days": min_trading_days
        }).execute()

        st.success("Funded rules saved.")
