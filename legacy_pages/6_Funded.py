import streamlit as st
from utils.supabase_client import get_supabase_client
from dashboard.funded_tracker import show_funded_tracker

st.title("💰 Funded Accounts")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

accounts_response = supabase.table("accounts").select("*").execute()
rules_response = supabase.table("funded_rules").select("*").execute()

accounts = accounts_response.data
rules = rules_response.data

show_funded_tracker(accounts, rules)
