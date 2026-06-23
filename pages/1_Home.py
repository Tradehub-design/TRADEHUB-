import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats

st.title("🏠 Home")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()

df = prepare_trades_dataframe(response.data)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

stats = summary_stats(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Trades", stats["total_trades"])

with col2:
    st.metric("Net Profit", round(stats["net_profit"],2))

with col3:
    st.metric("Wins", stats["wins"])

with col4:
    st.metric("Win Rate", f"{stats['win_rate']}%")

st.divider()

st.write("📈 Equity Curve Coming Soon")
st.write("📅 Calendar Heatmap Coming Soon")
st.write("🔥 Best Setups Coming Soon")
st.write("⚠️ Drawdown Analysis Coming Soon")
