import streamlit as st
import pandas as pd
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe
from utils.calendar_utils import daily_trade_summary
from dashboard.calendar_heatmap import show_calendar_heatmap

st.title("📅 Calendar")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
data = response.data

df = prepare_trades_dataframe(data)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

daily = daily_trade_summary(df)

show_calendar_heatmap(daily)

st.subheader("Daily Summary")
st.dataframe(daily, use_container_width=True)

st.divider()

st.subheader("Calendar Heatmap Coming Next")
