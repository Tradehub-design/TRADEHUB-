import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe

st.title("🤖 AI Coach")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
df = prepare_trades_dataframe(response.data)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

question = st.text_area(
    "Ask TradeHub about your trading",
    placeholder="Example: Why am I losing on Gold? Which session performs best?"
)

if st.button("Analyze"):
    st.info("AI analysis will be added later.")

st.divider()

st.subheader("Quick Insights")

losing_trades = df[df["net_profit"] < 0]
winning_trades = df[df["net_profit"] > 0]

st.write(f"Losing trades: {len(losing_trades)}")
st.write(f"Winning trades: {len(winning_trades)}")

if "symbol" in df.columns:
    st.write("Worst symbols by P/L:")
    worst_symbols = df.groupby("symbol")["net_profit"].sum().sort_values().head(5)
    st.dataframe(worst_symbols)
