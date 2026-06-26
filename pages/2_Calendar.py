import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine


load_css()

app_header(
    "📅 Calendar",
    "Review trading activity by date and prepare for daily planning."
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
        "value": stats["net_profit"],
        "helper": "Total closed result",
        "status": "positive" if stats["net_profit"] >= 0 else "negative",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Overall win rate",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
])

section("Recent Trading Dates")

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

table_header(
    "Recent Trades",
    "Calendar view will become more detailed once daily planning is connected."
)

st.dataframe(
    trades[display_cols].head(30),
    use_container_width=True,
    hide_index=True
)
