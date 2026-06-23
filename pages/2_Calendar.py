import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe
from utils.calendar_utils import daily_trade_summary
from dashboard.calendar_heatmap import show_calendar_heatmap
from dashboard.filter_panel import account_filter

st.title("📅 Calendar")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
df = prepare_trades_dataframe(response.data)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

df, selected_account = account_filter(df)

daily = daily_trade_summary(df)

show_calendar_heatmap(daily)
