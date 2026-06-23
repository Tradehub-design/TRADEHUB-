import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe
from dashboard.trade_cards import show_trade_card
from dashboard.filter_panel import account_filter, trade_filters

st.title("📒 Journal")

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

st.subheader("Trade Cards")

for _, trade in df.iterrows():
    show_trade_card(trade.to_dict())
