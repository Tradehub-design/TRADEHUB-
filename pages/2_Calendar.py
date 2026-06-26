import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine


load_css()

app_header(
    "📅 Calendar",
    "Review trading activity by day and month."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using the Calendar.",
        "Daily activity will appear here."
    )
    st.stop()

stats = StatisticsEngine.summary(trades)

section("Calendar Summary")

stat_row([
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "Imported history",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": FormatEngine.signed_currency(stats["net_profit"]),
        "helper": "Total closed result",
        "status": FormatEngine.result_status(stats["net_profit"]),
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Overall win rate",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
])

if "trade_date" not in trades.columns:
    command_card(
        "No trade date column",
        "Calendar needs a trade_date column to group trades by day.",
        "Check your import mapping."
    )
    st.stop()

temp = trades.copy()
temp["trade_date"] = pd.to_datetime(temp["trade_date"], errors="coerce")
temp = temp.dropna(subset=["trade_date"])

if temp.empty:
    command_card(
        "No valid trade dates",
        "Trade dates could not be parsed.",
        "Check your import data."
    )
    st.stop()

temp["Day"] = temp["trade_date"].dt.date
temp["Month"] = temp["trade_date"].dt.strftime("%Y-%m")

daily = (
    temp.groupby("Day")
    .agg(
        Trades=("Day", "count"),
        NetProfit=("net_profit", "sum"),
        Wins=("net_profit", lambda x: (x > 0).sum()),
    )
    .reset_index()
    .sort_values("Day", ascending=False)
)

daily["WinRate"] = (daily["Wins"] / daily["Trades"] * 100).round(1)

monthly = (
    temp.groupby("Month")
    .agg(
        Trades=("Month", "count"),
        NetProfit=("net_profit", "sum"),
        Wins=("net_profit", lambda x: (x > 0).sum()),
    )
    .reset_index()
    .sort_values("Month", ascending=False)
)

monthly["WinRate"] = (monthly["Wins"] / monthly["Trades"] * 100).round(1)

section("Monthly Calendar")

table_header(
    "Monthly Results",
    "Trade performance grouped by month."
)

st.dataframe(
    monthly,
    use_container_width=True,
    hide_index=True
)

section("Daily Calendar")

table_header(
    "Daily Results",
    "Trade performance grouped by day."
)

st.dataframe(
    daily,
    use_container_width=True,
    hide_index=True
)

section("Recent Trades")

display_cols = [
    col for col in [
        "ticket",
        "trade_date",
        "symbol",
        "direction",
        "net_profit",
        "session",
    ]
    if col in trades.columns
]

st.dataframe(
    trades[display_cols].head(30),
    use_container_width=True,
    hide_index=True
)
