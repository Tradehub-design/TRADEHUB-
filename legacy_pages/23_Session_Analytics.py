import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from components.trade_table import TradeTable


load_css()

app_header(
    "🕒 Session Analytics",
    "Compare Asia, London and New York performance."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card("No trades found", "Import trades first.", "Waiting for data.")
    st.stop()

if "session" not in trades.columns:
    command_card("No session data", "Session column is required.", "Check trade data.")
    st.stop()

sessions = sorted(trades["session"].dropna().unique().tolist())
selected = st.selectbox("Select Session", ["All"] + sessions)

session_trades = trades.copy()

if selected != "All":
    session_trades = session_trades[session_trades["session"] == selected]

stats = StatisticsEngine.summary(session_trades)

section("Session Summary")

stat_row([
    {"label": "Trades", "value": stats["total_trades"], "helper": "Filtered trades", "status": "neutral"},
    {"label": "Net Profit", "value": FormatEngine.signed_currency(stats["net_profit"]), "helper": "Session result", "status": FormatEngine.result_status(stats["net_profit"])},
    {"label": "Win Rate", "value": f"{stats['win_rate']}%", "helper": "Wins", "status": "positive" if stats["win_rate"] >= 50 else "negative"},
    {"label": "Profit Factor", "value": stats["profit_factor"], "helper": "Gross profit/loss", "status": "positive" if stats["profit_factor"] >= 1 else "negative"},
])

section("Session Leaderboard")

summary = (
    trades.groupby("session")
    .agg(
        Trades=("session", "count"),
        NetProfit=("net_profit", "sum"),
        Wins=("net_profit", lambda x: (x > 0).sum()),
    )
    .reset_index()
)

summary["WinRate"] = (summary["Wins"] / summary["Trades"] * 100).round(1)
summary["NetProfit"] = summary["NetProfit"].round(2)

table_header("Sessions", "Performance by trading session")

st.dataframe(summary, use_container_width=True, hide_index=True)

section("Trades")

TradeTable.render(session_trades, height=600)
