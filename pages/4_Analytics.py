import streamlit as st

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header, mini_card
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.analytics_engine import AnalyticsEngine
from engine.health_engine import HealthEngine


load_css()

app_header(
    "📊 Analytics Pro",
    "Study performance by symbol, session, month and trading health."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using Analytics Pro.",
        "Go to Import."
    )
    st.stop()

stats = StatisticsEngine.summary(trades)
health_score = HealthEngine.score(trades)
health_grade = HealthEngine.grade(health_score)

section("Account Performance")

stat_row([
    {
        "label": "Net Profit",
        "value": stats["net_profit"],
        "helper": "Total closed result",
        "status": "positive" if stats["net_profit"] >= 0 else "negative",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": f"{stats['wins']} wins / {stats['total_trades']} trades",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
    {
        "label": "Profit Factor",
        "value": stats["profit_factor"],
        "helper": "Gross profit / gross loss",
        "status": "positive" if stats["profit_factor"] >= 1 else "negative",
    },
    {
        "label": "Trading Health",
        "value": health_score,
        "helper": f"Grade {health_grade}",
        "status": "positive" if health_score >= 75 else "warning",
    },
])

stat_row([
    {
        "label": "Average Trade",
        "value": stats["average_trade"],
        "helper": "Average closed result",
        "status": "positive" if stats["average_trade"] >= 0 else "negative",
    },
    {
        "label": "Average Win",
        "value": stats["average_win"],
        "helper": "Average winning trade",
        "status": "positive",
    },
    {
        "label": "Average Loss",
        "value": stats["average_loss"],
        "helper": "Average losing trade",
        "status": "negative",
    },
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "Imported trades",
        "status": "neutral",
    },
])

section("Performance Curve")

monthly = AnalyticsEngine.monthly_summary(trades)

if monthly.empty:
    command_card(
        "No monthly performance yet",
        "Monthly analytics will appear once trade dates are available.",
        "Check your import date field."
    )
else:
    st.line_chart(
        monthly.set_index("Month")["NetProfit"]
    )

    table_header(
        "Monthly Results",
        "Performance grouped by calendar month."
    )

    st.dataframe(
        monthly,
        use_container_width=True,
        hide_index=True
    )

section("Performance Intelligence")

symbol_summary = AnalyticsEngine.symbol_summary(trades)
session_summary = AnalyticsEngine.session_summary(trades)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if not symbol_summary.empty:
        row = symbol_summary.iloc[0]
        mini_card(
            "Best Symbol",
            row["symbol"],
            f"Net {round(row['NetProfit'], 2)}",
            "positive",
            "🏆"
        )
    else:
        mini_card("Best Symbol", "N/A", "Insufficient data", "neutral", "🏆")

with col2:
    if not symbol_summary.empty:
        row = symbol_summary.iloc[-1]
        mini_card(
            "Worst Symbol",
            row["symbol"],
            f"Net {round(row['NetProfit'], 2)}",
            "negative",
            "⚠️"
        )
    else:
        mini_card("Worst Symbol", "N/A", "Insufficient data", "neutral", "⚠️")

with col3:
    if not session_summary.empty:
        row = session_summary.iloc[0]
        mini_card(
            "Best Session",
            row["session"],
            f"Net {round(row['NetProfit'], 2)}",
            "positive",
            "☀️"
        )
    else:
        mini_card("Best Session", "N/A", "Insufficient data", "neutral", "☀️")

with col4:
    if not session_summary.empty:
        row = session_summary.iloc[-1]
        mini_card(
            "Worst Session",
            row["session"],
            f"Net {round(row['NetProfit'], 2)}",
            "negative",
            "🌙"
        )
    else:
        mini_card("Worst Session", "N/A", "Insufficient data", "neutral", "🌙")

section("Symbol Leaderboard")

if symbol_summary.empty:
    st.info("No symbol data available.")
else:
    table_header(
        "Symbols",
        "Your strongest and weakest traded instruments."
    )

    st.dataframe(
        symbol_summary,
        use_container_width=True,
        hide_index=True
    )

section("Session Leaderboard")

if session_summary.empty:
    st.info("No session data available.")
else:
    table_header(
        "Sessions",
        "Your performance by trading session."
    )

    st.dataframe(
        session_summary,
        use_container_width=True,
        hide_index=True
    )
