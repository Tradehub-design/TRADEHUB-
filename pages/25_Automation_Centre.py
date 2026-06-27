import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row
from data.data_engine import DataEngine


load_css()

app_header(
    "⚙️ Automation Centre",
    "Monitor MT5 Sync, screenshot watchers and background services."
)

sync_status = DataEngine.load_sync_status()
open_positions = DataEngine.load_open_positions()
account_snapshot = DataEngine.load_account_snapshot()

section("Automation Status")

if sync_status.empty:
    stat_row([
        {"label": "MT5 Sync", "value": "Offline", "helper": "No sync detected", "status": "warning"},
        {"label": "Open Positions", "value": len(open_positions), "helper": "Live table", "status": "neutral"},
        {"label": "Account Data", "value": "Waiting", "helper": "No snapshot", "status": "warning"},
    ])
else:
    row = sync_status.iloc[0]

    stat_row([
        {"label": "MT5 Sync", "value": row.get("status", "unknown"), "helper": row.get("message", ""), "status": "positive" if row.get("status") == "connected" else "warning"},
        {"label": "Last Sync", "value": row.get("last_sync", "-"), "helper": "Desktop agent", "status": "neutral"},
        {"label": "Open Positions", "value": len(open_positions), "helper": "Live positions", "status": "positive"},
    ])

section("Automation Modules")

command_card(
    "MT5 Sync Agent",
    "Syncs account balance, equity, open positions and closed trades.",
    "Run locally on Windows."
)

command_card(
    "Screenshot Watcher",
    "Watches folders and uploads matched screenshots to TradeHub.",
    "Runs locally on computer."
)

command_card(
    "TradingView Watcher",
    "Imports TradingView screenshots and attaches them to trades.",
    "Runs locally on computer."
)

section("Live Account Snapshot")

if account_snapshot.empty:
    command_card("No snapshot", "Run the sync agent to see live account data.", "Waiting.")
else:
    st.dataframe(account_snapshot, use_container_width=True, hide_index=True)
