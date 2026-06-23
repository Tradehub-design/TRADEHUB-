import streamlit as st
import pandas as pd
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats
from dashboard.filter_panel import account_filter, trade_filters

st.title("📈 Trades")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
data = response.data

df = prepare_trades_dataframe(data)

df, selected_account = account_filter(df)
df = trade_filters(df)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

stats = summary_stats(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Trades", stats["total_trades"])

with col2:
    st.metric("Net Profit", stats["net_profit"])

with col3:
    st.metric("Wins", stats["wins"])

with col4:
    st.metric("Win Rate", f"{stats['win_rate']}%")

st.divider()

st.dataframe(df, use_container_width=True)
