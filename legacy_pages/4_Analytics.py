import streamlit as st

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header, mini_card
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.analytics_engine import AnalyticsEngine
from engine.advanced_metrics_engine import AdvancedMetricsEngine
from engine.format_engine import FormatEngine


load_css()

app_header(
    "📊 Analytics Pro",
    "Deep performance analytics using your real trade history."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using analytics.",
        "Waiting for trade data."
    )
    st.stop()

stats = StatisticsEngine.summary(trades)
advanced = AdvancedMetricsEngine.summary(trades)

section("Performance Summary")

stat_row([
    {
        "label": "Net Profit",
        "value": FormatEngine.signed_currency(stats["net_profit"]),
        "helper": "Total closed result",
        "status": FormatEngine.result_status(stats["net_profit"]),
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
        "helper": "Gross profit / loss",
        "status": "positive" if stats["profit_factor"] >= 1 else "negative",
    },
    {
        "label": "Average Trade",
        "value": FormatEngine.signed_currency(stats["average_trade"]),
        "helper": "Expectancy style result",
        "status": FormatEngine.result_status(stats["average_trade"]),
    },
])

section("Advanced Metrics")

stat_row([
    {
        "label": "Best Trade",
        "value": FormatEngine.signed_currency(advanced["best_trade"]),
        "helper": "Largest single win",
        "status": "positive",
    },
    {
        "label": "Worst Trade",
        "value": FormatEngine.signed_currency(advanced["worst_trade"]),
        "helper": "Largest single loss",
        "status": "negative",
    },
    {
        "label": "Avg Hold",
        "value": f"{advanced['average_hold_minutes']}m",
        "helper": "Average holding time",
        "status": "neutral",
    },
    {
        "label": "Most Traded",
        "value": advanced["most_traded_symbol"],
        "helper": "Highest trade count",
        "status": "neutral",
    },
])

section("Performance Curve")

monthly = AnalyticsEngine.monthly_summary(trades)

if monthly.empty:
    command_card(
        "No monthly data",
        "Monthly performance requires valid trade dates.",
        "Check import mapping."
    )
else:
    st.line_chart(
        monthly.set_index("Month")["NetProfit"]
    )

    table_header(
        "Monthly Performance",
        "Grouped by month"
    )

    st.dataframe(
        monthly,
        use_container_width=True,
        hide_index=True
    )

section("Symbol Intelligence")

symbol_summary = AnalyticsEngine.symbol_summary(trades)

if symbol_summary.empty:
    st.info("No symbol data available.")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        best = symbol_summary.iloc[0]
        mini_card(
            "Best Symbol",
            best["symbol"],
            FormatEngine.signed_currency(best["NetProfit"]),
            "positive",
            "🏆"
        )

    with col2:
        worst = symbol_summary.iloc[-1]
        mini_card(
            "Worst Symbol",
            worst["symbol"],
            FormatEngine.signed_currency(worst["NetProfit"]),
            "negative",
            "⚠️"
        )

    with col3:
        mini_card(
            "Largest Symbol",
            advanced["largest_symbol"],
            "Highest total profit",
            "positive",
            "📈"
        )

    table_header(
        "Symbol Leaderboard",
        "Performance by pair"
    )

    st.dataframe(
        symbol_summary,
        use_container_width=True,
        hide_index=True
    )

section("Session Intelligence")

session_summary = AnalyticsEngine.session_summary(trades)

if session_summary.empty:
    st.info("No session data available.")
else:
    table_header(
        "Session Leaderboard",
        "Performance by trading session"
    )

    st.dataframe(
        session_summary,
        use_container_width=True,
        hide_index=True
    )
