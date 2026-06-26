import streamlit as st

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.analytics_engine import AnalyticsEngine


load_css()

app_header(
    "📊 Analytics Pro",
    "Analyse performance by symbol, session and month."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using Analytics.",
        "Go to Import."
    )
    st.stop()

stats = StatisticsEngine.summary(trades)

section("Account Performance")

stat_row([
    {
        "label": "Net Profit",
        "value": stats["net_profit"],
        "helper": "Total result",
        "status": "positive" if stats["net_profit"] >= 0 else "negative",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Winning percentage",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
    {
        "label": "Profit Factor",
        "value": stats["profit_factor"],
        "helper": "Gross profit / loss",
        "status": "positive" if stats["profit_factor"] >= 1 else "negative",
    },
])

stat_row([
    {
        "label": "Average Win",
        "value": stats["average_win"],
        "helper": "Winning trades",
        "status": "positive",
    },
    {
        "label": "Average Loss",
        "value": stats["average_loss"],
        "helper": "Losing trades",
        "status": "negative",
    },
    {
        "label": "Average Trade",
        "value": stats["average_trade"],
        "helper": "Expected average",
        "status": "positive" if stats["average_trade"] >= 0 else "negative",
    },
])

section("Monthly Performance")

monthly = AnalyticsEngine.monthly_summary(trades)

if monthly.empty:
    st.info("No monthly performance data available.")
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

section("Symbol Leaderboard")

symbol_summary = AnalyticsEngine.symbol_summary(trades)

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

session_summary = AnalyticsEngine.session_summary(trades)

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

section("Best / Worst Summary")

if not symbol_summary.empty:
    best_symbol = symbol_summary.iloc[0]
    worst_symbol = symbol_summary.iloc[-1]

    stat_row([
        {
            "label": "Best Symbol",
            "value": best_symbol["symbol"],
            "helper": f"Net {round(best_symbol['NetProfit'], 2)}",
            "status": "positive",
        },
        {
            "label": "Worst Symbol",
            "value": worst_symbol["symbol"],
            "helper": f"Net {round(worst_symbol['NetProfit'], 2)}",
            "status": "negative",
        },
    ])

if not session_summary.empty:
    best_session = session_summary.iloc[0]
    worst_session = session_summary.iloc[-1]

    stat_row([
        {
            "label": "Best Session",
            "value": best_session["session"],
            "helper": f"Net {round(best_session['NetProfit'], 2)}",
            "status": "positive",
        },
        {
            "label": "Worst Session",
            "value": worst_session["session"],
            "helper": f"Net {round(worst_session['NetProfit'], 2)}",
            "status": "negative",
        },
    ])
