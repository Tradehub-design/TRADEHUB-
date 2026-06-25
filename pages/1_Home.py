import streamlit as st

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats
from core.ui import load_css, app_header, section
from core.components import stat_row, command_card
from dashboard.equity_curve import show_equity_curve
from dashboard.drawdown_analysis import show_drawdown_analysis
from dashboard.account_analysis import show_account_analysis

load_css()

app_header(
    "🏠 Command Centre",
    "Your daily trading cockpit — performance, risk, accounts and coaching insight."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = supabase.table("trades").select("*").execute()
df = prepare_trades_dataframe(response.data)

if df.empty:
    command_card(
        "No trades found yet",
        "Import trades or add a test trade to activate your dashboard.",
        "Next step: Import your broker history."
    )
    st.stop()

stats = summary_stats(df)

net_profit = stats["net_profit"]
profit_status = "positive" if net_profit >= 0 else "negative"

section("Performance Snapshot")

stat_row([
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "All imported trades",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": net_profit,
        "helper": "Realised result",
        "status": profit_status,
    },
])

stat_row([
    {
        "label": "Winning Trades",
        "value": stats["wins"],
        "helper": "Closed in profit",
        "status": "positive",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Wins / total trades",
        "status": "neutral",
    },
])

section("AI Coach")

if stats["win_rate"] >= 60:
    ai_message = "Your current win rate is strong. Next focus: increase average win size and avoid overtrading after profitable trades."
elif stats["win_rate"] >= 45:
    ai_message = "Your win rate is moderate. Next focus: identify your best session, best symbol and best setup, then reduce lower-quality trades."
else:
    ai_message = "Your win rate needs work. Next focus: reduce trade frequency, journal every mistake, and only take A-grade setups."

command_card(
    "🤖 Daily Trading Insight",
    ai_message,
    "This will become personalised as more trades are imported."
)

section("Equity Curve")
show_equity_curve(df)

section("Drawdown")
show_drawdown_analysis(df)

section("Account Performance")
show_account_analysis(df)
