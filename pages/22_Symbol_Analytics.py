import streamlit as st

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.analytics_engine import AnalyticsEngine
from engine.format_engine import FormatEngine
from components.trade_table import TradeTable


load_css()

app_header(
    "💱 Symbol Analytics",
    "Study each pair individually to find where your real edge is."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using Symbol Analytics.",
        "Waiting for trade data."
    )
    st.stop()

if "symbol" not in trades.columns:
    command_card(
        "No symbol column",
        "Symbol analytics needs a symbol column.",
        "Check your trade data."
    )
    st.stop()

symbols = sorted(trades["symbol"].dropna().unique().tolist())

selected_symbol = st.selectbox(
    "Select Symbol",
    symbols
)

symbol_trades = trades[
    trades["symbol"] == selected_symbol
]

stats = StatisticsEngine.summary(symbol_trades)

section(f"{selected_symbol} Summary")

stat_row([
    {
        "label": "Trades",
        "value": stats["total_trades"],
        "helper": "Total trades",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": FormatEngine.signed_currency(stats["net_profit"]),
        "helper": "Symbol result",
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
        "helper": "Gross profit / loss",
        "status": "positive" if stats["profit_factor"] >= 1 else "negative",
    },
])

section("Monthly Symbol Performance")

monthly = AnalyticsEngine.monthly_summary(symbol_trades)

if monthly.empty:
    st.info("No monthly symbol data available.")
else:
    st.line_chart(
        monthly.set_index("Month")["NetProfit"]
    )

section("Direction Split")

if "direction" in symbol_trades.columns:
    direction_summary = (
        symbol_trades.groupby("direction")
        .agg(
            Trades=("direction", "count"),
            NetProfit=("net_profit", "sum"),
            Wins=("net_profit", lambda x: (x > 0).sum()),
        )
        .reset_index()
    )

    direction_summary["WinRate"] = (
        direction_summary["Wins"] / direction_summary["Trades"] * 100
    ).round(1)

    table_header(
        "Direction Performance",
        "BUY vs SELL performance"
    )

    st.dataframe(
        direction_summary,
        use_container_width=True,
        hide_index=True
    )

section("Trades")

table_header(
    f"{selected_symbol} Trades",
    f"{len(symbol_trades)} trades"
)

TradeTable.render(
    symbol_trades,
    height=560
)
