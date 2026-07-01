import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.live_account_health_engine import LiveAccountHealthEngine
from engine.format_engine import FormatEngine


load_css()

app_header(
    "🟢 Live Account",
    "Monitor live MT5 balance, equity, margin and open positions."
)

account_snapshot = DataEngine.load_account_snapshot()
open_positions = DataEngine.load_open_positions()
sync_status = DataEngine.load_sync_status()

health = LiveAccountHealthEngine.calculate(
    account_snapshot,
    open_positions
)

section("Connection Status")

if sync_status is None or sync_status.empty:
    stat_row([
        {
            "label": "MT5 Sync",
            "value": "Offline",
            "helper": "No desktop sync detected",
            "status": "warning",
        },
        {
            "label": "Account",
            "value": health["status"],
            "helper": "Live account snapshot",
            "status": "warning",
        },
        {
            "label": "Risk",
            "value": health["risk_status"],
            "helper": "Margin health",
            "status": "neutral",
        },
    ])
else:
    row = sync_status.iloc[0]

    stat_row([
        {
            "label": "MT5 Sync",
            "value": row.get("status", "unknown"),
            "helper": row.get("message", ""),
            "status": "positive" if row.get("status") == "connected" else "warning",
        },
        {
            "label": "Last Sync",
            "value": row.get("last_sync", "-"),
            "helper": "Desktop sync agent",
            "status": "neutral",
        },
        {
            "label": "Risk",
            "value": health["risk_status"],
            "helper": "Margin health",
            "status": "positive" if health["risk_status"] in ["Healthy", "No Margin Used"] else "warning",
        },
    ])

section("Live Account Metrics")

stat_row([
    {
        "label": "Balance",
        "value": FormatEngine.currency(health["balance"]),
        "helper": "MT5 account balance",
        "status": "neutral",
    },
    {
        "label": "Equity",
        "value": FormatEngine.currency(health["equity"]),
        "helper": "Balance + floating P/L",
        "status": "positive" if health["equity"] >= health["balance"] else "negative",
    },
    {
        "label": "Floating P/L",
        "value": FormatEngine.signed_currency(health["floating_pl"]),
        "helper": "Open trade result",
        "status": FormatEngine.result_status(health["floating_pl"]),
    },
    {
        "label": "Margin Level",
        "value": f"{health['margin_level']}%",
        "helper": "Account safety",
        "status": "positive" if health["margin_level"] >= 500 or health["margin_level"] == 0 else "warning",
    },
])

section("Open Positions")

if open_positions is None or open_positions.empty:
    command_card(
        "No open positions",
        "Open positions will appear here once MT5 Sync detects live trades.",
        "Keep the sync agent running on your Windows computer."
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
