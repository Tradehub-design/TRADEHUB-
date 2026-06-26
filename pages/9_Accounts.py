import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.analytics_engine import AnalyticsEngine


load_css()

app_header(
    "💼 Accounts",
    "Manage trading accounts and review account-level performance."
)

trades = DataEngine.load_trades()

if trades is None or trades.empty:
    command_card(
        "No account data yet",
        "Import trades first to activate account analytics.",
        "MT5 Sync will later update this automatically."
    )
    st.stop()

section("Account Overview")

stats = StatisticsEngine.summary(trades)

stat_row([
    {
        "label": "Account",
        "value": "Fusion Markets",
        "helper": "Default account",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": stats["net_profit"],
        "helper": "Closed result",
        "status": "positive" if stats["net_profit"] >= 0 else "negative",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Winning percentage",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
])

stat_row([
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "Imported trades",
        "status": "neutral",
    },
    {
        "label": "Profit Factor",
        "value": stats["profit_factor"],
        "helper": "Gross profit / gross loss",
        "status": "positive" if stats["profit_factor"] >= 1 else "negative",
    },
    {
        "label": "Average Trade",
        "value": stats["average_trade"],
        "helper": "Average closed result",
        "status": "positive" if stats["average_trade"] >= 0 else "negative",
    },
])

section("Account Performance")

monthly = AnalyticsEngine.monthly_summary(trades)

if monthly.empty:
    st.info("Monthly account performance will appear once trade dates are available.")
else:
    st.line_chart(
        monthly.set_index("Month")["NetProfit"]
    )

    table_header(
        "Monthly Account Results",
        "Performance grouped by month."
    )

    st.dataframe(
        monthly,
        use_container_width=True,
        hide_index=True
    )

section("MT5 Sync Readiness")

command_card(
    "MT5 Sync Ready",
    "This page is ready to receive live balance, equity, margin and open-position data once the desktop sync agent is connected.",
    "For now, it uses your imported trade history."
)
