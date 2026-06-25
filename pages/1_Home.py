import streamlit as st

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats
from utils.ui import load_css, page_header, metric_card, section_title, info_card
from dashboard.equity_curve import show_equity_curve
from dashboard.drawdown_analysis import show_drawdown_analysis
from dashboard.account_analysis import show_account_analysis

load_css()

page_header(
    "🏠 Dashboard",
    "Your trading command centre — performance, risk, accounts and insights."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
df = prepare_trades_dataframe(response.data)

if df.empty:
    info_card(
        "No trades found yet",
        "Once trades are imported, this dashboard will show your profit, win rate, drawdown, accounts and trading insights."
    )
    st.stop()

stats = summary_stats(df)

net_profit = stats["net_profit"]
profit_status = "positive" if net_profit >= 0 else "negative"

section_title("Performance Overview")

col1, col2 = st.columns(2)

with col1:
    metric_card("Total Trades", stats["total_trades"])
    metric_card("Winning Trades", stats["wins"], "positive")

with col2:
    metric_card("Net Profit", net_profit, profit_status)
    metric_card("Win Rate", f"{stats['win_rate']}%", "neutral")

st.divider()

section_title("Equity Curve")
show_equity_curve(df)

st.divider()

section_title("Drawdown")
show_drawdown_analysis(df)

st.divider()

section_title("Account Performance")
show_account_analysis(df)

st.divider()

section_title("AI Insight Preview")

if stats["win_rate"] >= 60:
    insight = "Your current win rate is strong. The next focus should be improving risk-to-reward and reducing avoidable losses."
elif stats["win_rate"] >= 45:
    insight = "Your win rate is moderate. Focus on filtering lower-quality setups and reviewing losing trades for repeated mistakes."
else:
    insight = "Your win rate is low. Focus on reducing trade frequency, improving setup quality, and tracking rule-breaking behaviour."

info_card("Trading Insight", insight)
