import streamlit as st

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats
from utils.ui import load_css, page_header, metric_card, section_title, insight_card
from dashboard.equity_curve import show_equity_curve
from dashboard.drawdown_analysis import show_drawdown_analysis
from dashboard.account_analysis import show_account_analysis

load_css()

page_header(
    "🏠 Dashboard",
    "A clean overview of your trading performance, risk, equity and AI insight."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
df = prepare_trades_dataframe(response.data)

if df.empty:
    insight_card(
        "No trades found yet",
        "Import trades or add a test trade to start building your trading analytics dashboard."
    )
    st.stop()

stats = summary_stats(df)

net_profit = stats["net_profit"]
profit_status = "positive" if net_profit >= 0 else "negative"

section_title("Today’s Command Centre")

col1, col2 = st.columns(2)

with col1:
    metric_card(
        "Total Trades",
        stats["total_trades"],
        "neutral",
        "All imported trades"
    )

    metric_card(
        "Winning Trades",
        stats["wins"],
        "positive",
        "Trades closed in profit"
    )

with col2:
    metric_card(
        "Net Profit",
        net_profit,
        profit_status,
        "Total realised net result"
    )

    metric_card(
        "Win Rate",
        f"{stats['win_rate']}%",
        "neutral",
        "Winning trades / total trades"
    )

st.divider()

if stats["win_rate"] >= 60:
    ai_message = "Your current win rate is strong. Next focus: improve average win size and protect against overtrading after wins."
elif stats["win_rate"] >= 45:
    ai_message = "Your win rate is moderate. Next focus: identify which setups and sessions perform best, then reduce lower-quality trades."
else:
    ai_message = "Your win rate needs improvement. Next focus: reduce trade frequency, track mistakes, and only take A-grade setups."

insight_card(
    "🤖 AI Coach Preview",
    ai_message
)

st.divider()

section_title("Equity Curve")
show_equity_curve(df)

st.divider()

section_title("Drawdown")
show_drawdown_analysis(df)

st.divider()

section_title("Account Performance")
show_account_analysis(df)
