import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.calendar_engine import CalendarEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from components.trade_table import TradeTable


load_css()

app_header(
    "📅 Trading Calendar",
    "Review daily trading performance and click into trading days."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card("No trades found", "Import trades first.", "Waiting for data.")
    st.stop()

stats = StatisticsEngine.summary(trades)

section("Calendar Summary")

stat_row([
    {"label": "Trades", "value": stats["total_trades"], "helper": "All trades", "status": "neutral"},
    {"label": "Net Profit", "value": FormatEngine.signed_currency(stats["net_profit"]), "helper": "Total result", "status": FormatEngine.result_status(stats["net_profit"])},
    {"label": "Win Rate", "value": f"{stats['win_rate']}%", "helper": "Overall", "status": "positive" if stats["win_rate"] >= 50 else "negative"},
])

daily = CalendarEngine.daily_summary(trades)

if daily.empty:
    command_card("No calendar data", "Valid trade dates are required.", "Check import mapping.")
    st.stop()

section("Daily Results")

table_header("Daily Calendar", "Performance grouped by trading day")

st.dataframe(daily, use_container_width=True, hide_index=True)

days = daily["day"].astype(str).tolist()
selected_day = st.selectbox("Select Day", days)

day_trades = trades[
    trades["trade_date"].astype(str).str.startswith(selected_day)
]

section(f"Trades on {selected_day}")

TradeTable.render(day_trades, height=520)
