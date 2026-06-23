import streamlit as st
import pandas as pd
from utils.supabase_client import get_supabase_client

st.title("📊 Dashboard")

supabase = get_supabase_client()

response = supabase.table("trades").select("*").execute()

if response.data:
    df = pd.DataFrame(response.data)

    st.metric("Trades", len(df))

    if "profit" in df.columns:
        total_profit = round(df["profit"].sum(), 2)
        st.metric("Net Profit", f"${total_profit}")

    if "profit" in df.columns:
        win_rate = round(
            (df["profit"] > 0).mean() * 100,
            1
        )
        st.metric("Win Rate", f"{win_rate}%")

else:
    st.info("No trades yet.")
