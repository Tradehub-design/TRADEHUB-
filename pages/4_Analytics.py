import streamlit as st
import plotly.express as px
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe
from dashboard.filter_panel import account_filter, trade_filters

st.title("📊 Analytics")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
df = prepare_trades_dataframe(response.data)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

df, selected_account = account_filter(df)
df = trade_filters(df)

st.subheader("Symbol Performance")

symbol_perf = df.groupby("symbol")["net_profit"].sum().reset_index()
fig_symbol = px.bar(symbol_perf, x="symbol", y="net_profit", title="P/L by Symbol")
st.plotly_chart(fig_symbol, use_container_width=True)

st.subheader("Session Performance")

session_perf = df.groupby("session")["net_profit"].sum().reset_index()
fig_session = px.bar(session_perf, x="session", y="net_profit", title="P/L by Session")
st.plotly_chart(fig_session, use_container_width=True)

st.subheader("Strategy Performance")

strategy_perf = df.groupby("strategy")["net_profit"].sum().reset_index()
fig_strategy = px.bar(strategy_perf, x="strategy", y="net_profit", title="P/L by Strategy")
st.plotly_chart(fig_strategy, use_container_width=True)
