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
account_snapshot = DataEngine.load_account_snapshot()
open_positions = DataEngine.load_open_positions()

section("Live Account")

if account_snapshot.empty:
    command_card(
        "No live account data",
        "Run the MT5 Sync Agent on your Windows computer to activate live account tracking.",
        "For now, this page uses imported trade history."
    )
else:
    account = account_snapshot.iloc[0]

    stat_row([
        {
            "label": "Balance",
            "value": account.get("balance", 0),
            "helper": account.get("broker", "Broker"),
            "status": "neutral",
        },
        {
            "label": "Equity",
            "value": account.get("equity", 0),
            "helper": account.get("currency", ""),
            "status": "positive" if account.get("equity", 0) >= account.get("balance", 0) else "negative",
        },
        {
            "label": "Floating P/L",
            "value": account.get("profit", 0),
            "helper": "Open positions",
            "status": "positive" if account.get("profit", 0) >= 0 else "negative",
        },
    ])

    stat_row([
        {
            "label": "Margin",
            "value": account.get("margin", 0),
            "helper": "Used margin",
            "status": "neutral",
        },
        {
            "label": "Free Margin",
            "value": account.get("free_margin", 0),
            "helper": "Available",
            "status": "positive",
        },
        {
            "label": "Margin Level",
            "value": account.get("margin_level", 0),
            "helper": "Account safety",
            "status": "positive",
        },
    ])

section("Imported Performance")

if trades is None or trades.empty:
    command_card(
        "No imported trades",
        "Import trades or run MT5 Sync to activate account analytics.",
        "Waiting for data."
    )
else:
    stats = StatisticsEngine.summary(trades)

    stat_row([
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
        {
            "label": "Total Trades",
            "value": stats["total_trades"],
            "helper": "Imported trades",
            "status": "neutral",
        },
    ])

    monthly = AnalyticsEngine.monthly_summary(trades)

    if not monthly.empty:
        section("Monthly Performance")

        st.line_chart(
            monthly.set_index("Month")["NetProfit"]
        )

section("Open Positions")

if open_positions.empty:
    command_card(
        "No open positions",
        "Open positions will appear here once MT5 Sync is running.",
        "Live trading data."
    )
else:
    table_header(
        "Open Positions",
        f"{len(open_positions)} active positions"
    )

    st.dataframe(
        open_positions,
        use_container_width=True,
        hide_index=True
    )
