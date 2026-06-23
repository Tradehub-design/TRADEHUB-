import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats
from dashboard.filter_panel import account_filter, trade_filters

st.title("📈 Trades")

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

stats = summary_stats(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Trades", stats["total_trades"])
col2.metric("Net Profit", stats["net_profit"])
col3.metric("Wins", stats["wins"])
col4.metric("Win Rate", f"{stats['win_rate']}%")

st.divider()

columns_to_show = [
    "trade_date",
    "account_number",
    "symbol",
    "direction",
    "volume",
    "entry_price",
    "exit_price",
    "net_profit",
    "session",
    "strategy",
    "result",
]

available_columns = [col for col in columns_to_show if col in df.columns]

st.table(df[available_columns])
