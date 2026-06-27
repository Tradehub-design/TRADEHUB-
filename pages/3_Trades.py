import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from components.trade_filters import TradeFilters
from components.trade_table import TradeTable


load_css()

app_header(
    "📋 Trades",
    "Browse, filter and study your real trading history."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades or use the real trade seed data.",
        "Waiting for trade history."
    )
    st.stop()

stats = StatisticsEngine.summary(trades)

section("Trade Summary")

stat_row([
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "All loaded trades",
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
        "helper": f"{stats['wins']} wins",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
    {
        "label": "Profit Factor",
        "value": stats["profit_factor"],
        "helper": "Gross profit / gross loss",
        "status": "positive" if stats["profit_factor"] >= 1 else "negative",
    },
])

section("Filters")

filters = TradeFilters.render(
    trades,
    key_prefix="trades_page"
)

filtered = TradeFilters.apply(
    trades,
    filters
)

filtered_stats = StatisticsEngine.summary(filtered)

section("Filtered Result")

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

table_header(
    "Trades",
    f"{len(filtered)} matching trades"
)

TradeTable.render(
    filtered,
    height=620
)
