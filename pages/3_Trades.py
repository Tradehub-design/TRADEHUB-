import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine


load_css()

app_header(
    "📋 Trades",
    "Browse imported trades with clean filters and performance context."
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
        "value": stats["net_profit"],
        "helper": "Total result",
        "status": "positive" if stats["net_profit"] >= 0 else "negative",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Winning trades",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
])

section("Filters")

symbols = ["All"] + sorted(trades["symbol"].dropna().unique().tolist()) if "symbol" in trades.columns else ["All"]

col1, col2, col3 = st.columns(3)

with col1:
    symbol = st.selectbox("Symbol", symbols)

with col2:
    direction = st.selectbox("Direction", ["All", "BUY", "SELL"])

with col3:
    result = st.selectbox("Result", ["All", "Win", "Loss", "Breakeven"])

filtered = trades.copy()

if symbol != "All" and "symbol" in filtered.columns:
    filtered = filtered[filtered["symbol"] == symbol]

if direction != "All" and "direction" in filtered.columns:
    filtered = filtered[filtered["direction"] == direction]

if result == "Win":
    filtered = filtered[filtered["net_profit"] > 0]
elif result == "Loss":
    filtered = filtered[filtered["net_profit"] < 0]
elif result == "Breakeven":
    filtered = filtered[filtered["net_profit"] == 0]

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
