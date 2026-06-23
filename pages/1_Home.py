import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats
from dashboard.dashboard_summary import show_dashboard_summary
from dashboard.equity_curve import show_equity_curve

st.title("🏠 TradeHub Dashboard")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
df = prepare_trades_dataframe(response.data)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

stats = summary_stats(df)

show_dashboard_summary(stats)

st.divider()

show_equity_curve(df)
