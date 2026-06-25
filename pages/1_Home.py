import streamlit as st

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats
from utils.ui import load_css, page_header, metric_card
from dashboard.equity_curve import show_equity_curve
from dashboard.drawdown_analysis import show_drawdown_analysis
from dashboard.account_analysis import show_account_analysis

load_css()

page_header(
    "🏠 TradeHub Dashboard",
    "Your trading performance, equity, drawdown and account overview."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
df = prepare_trades_dataframe(response.data)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

stats = summary_stats(df)

profit_status = "positive" if stats["net_profit"] >= 0 else "negative"

col1, col2 = st.columns(2)

with col1:
    metric_card("Total Trades", stats["total_trades"])
    metric_card("Wins", stats["wins"], "positive")

with col2:
    metric_card("Net Profit", stats["net_profit"], profit_status)
    metric_card("Win Rate", f"{stats['win_rate']}%", "neutral")

st.divider()

show_equity_curve(df)

st.divider()

show_drawdown_analysis(df)

st.divider()

show_account_analysis(df)
