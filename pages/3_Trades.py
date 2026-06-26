import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine


load_css()

app_header(
    "📋 Trades",
    "Browse imported trades with filters, summaries and clean trade history."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using the Trades page.",
        "Go to Import."
    )
    st.stop()

stats = StatisticsEngine.summary(trades)

section("Trade Summary")

stat_row([
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "Imported records",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": FormatEngine.signed_currency(stats["net_profit"]),
        "helper": "Total result",
        "status": FormatEngine.result_status(stats["net_profit"]),
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Winning trades",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
    {
        "label": "Average Trade",
        "value": FormatEngine.signed_currency(stats["average_trade"]),
        "helper": "Average closed result",
        "status": FormatEngine.result_status(stats["average_trade"]),
    },
])

section("Filters")

symbols = ["All"] + sorted(trades["symbol"].dropna().unique().tolist()) if "symbol" in trades.columns else ["All"]
sessions = ["All"] + sorted(trades["session"].dropna().unique().tolist()) if "session" in trades.columns else ["All"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    symbol = st.selectbox("Symbol", symbols)

with col2:
    session = st.selectbox("Session", sessions)

with col3:
    direction = st.selectbox("Direction", ["All", "BUY", "SELL"])

with col4:
    result = st.selectbox("Result", ["All", "Win", "Loss", "Breakeven"])

filtered = trades.copy()

if symbol != "All" and "symbol" in filtered.columns:
    filtered = filtered[filtered["symbol"] == symbol]

if session != "All" and "session" in filtered.columns:
    filtered = filtered[filtered["session"] == session]

if direction != "All" and "direction" in filtered.columns:
    filtered = filtered[filtered["direction"] == direction]

if result == "Win":
    filtered = filtered[filtered["net_profit"] > 0]
elif result == "Loss":
    filtered = filtered[filtered["net_profit"] < 0]
elif result == "Breakeven":
    filtered = filtered[filtered["net_profit"] == 0]

section("Filtered Summary")

filtered_stats = StatisticsEngine.summary(filtered)

stat_row([
    {
        "label": "Matching Trades",
        "value": filtered_stats["total_trades"],
        "helper": "Current filter",
        "status": "neutral",
    },
    {
        "label": "Filtered Net",
        "value": FormatEngine.signed_currency(filtered_stats["net_profit"]),
        "helper": "Filtered result",
        "status": FormatEngine.result_status(filtered_stats["net_profit"]),
    },
    {
        "label": "Filtered Win Rate",
        "value": f"{filtered_stats['win_rate']}%",
        "helper": "Filtered wins",
        "status": "positive" if filtered_stats["win_rate"] >= 50 else "negative",
    },
])

section("Trade List")

display_cols = [
    col for col in [
        "ticket",
        "trade_date",
        "symbol",
        "direction",
        "volume",
        "entry_price",
        "exit_price",
        "net_profit",
        "session",
    ]
    if col in filtered.columns
]

table_header(
    "Trades",
    f"{len(filtered)} matching trades"
)

st.dataframe(
    filtered[display_cols],
    use_container_width=True,
    hide_index=True
)
