import streamlit as st

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header
from data.data_engine import DataEngine
from risk.risk_engine import RiskEngine
from engine.statistics_engine import StatisticsEngine


load_css()

app_header(
    "🛡 Risk Centre",
    "Protect capital, monitor losses and understand your risk profile."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using Risk Centre.",
        "Risk analytics will appear once trades are available."
    )
    st.stop()

risk = RiskEngine.calculate(trades)
stats = StatisticsEngine.summary(trades)

section("Risk Snapshot")

stat_row([
    {
        "label": "Recent Daily",
        "value": risk["daily"],
        "helper": "Recent trade sample",
        "status": "positive" if risk["daily"] >= 0 else "negative",
    },
    {
        "label": "Recent Weekly",
        "value": risk["weekly"],
        "helper": "Recent trade sample",
        "status": "positive" if risk["weekly"] >= 0 else "negative",
    },
    {
        "label": "Recent Monthly",
        "value": risk["monthly"],
        "helper": "Recent trade sample",
        "status": "positive" if risk["monthly"] >= 0 else "negative",
    },
])

section("Loss Control")

stat_row([
    {
        "label": "Largest Loss",
        "value": risk["largest_loss"],
        "helper": "Worst closed trade",
        "status": "negative",
    },
    {
        "label": "Average Loss",
        "value": risk["average_loss"],
        "helper": "Average losing trade",
        "status": "negative",
    },
    {
        "label": "Gross Loss",
        "value": stats["gross_loss"],
        "helper": "Total losing result",
        "status": "negative",
    },
])

section("Reward Profile")

stat_row([
    {
        "label": "Largest Win",
        "value": risk["largest_win"],
        "helper": "Best closed trade",
        "status": "positive",
    },
    {
        "label": "Average Win",
        "value": risk["average_win"],
        "helper": "Average winning trade",
        "status": "positive",
    },
    {
        "label": "Gross Profit",
        "value": stats["gross_profit"],
        "helper": "Total winning result",
        "status": "positive",
    },
])

section("Risk Notes")

command_card(
    "Risk Centre Status",
    "This page currently calculates risk from closed trade history. Once MT5 Sync is connected, it will include live exposure, floating P/L, margin and daily loss tracking.",
    "Use this page to identify whether losses are controlled."
)

section("Worst Recent Trades")

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

worst_trades = trades.sort_values(
    "net_profit",
    ascending=True
).head(10)

table_header(
    "Worst Trades",
    "Review these trades carefully in Trade Replay."
)

st.dataframe(
    worst_trades[display_cols],
    use_container_width=True,
    hide_index=True
)
