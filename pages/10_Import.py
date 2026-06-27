import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine


load_css()

app_header(
    "📥 Import Centre",
    "Import MT5 history, CSV files, TradingView screenshots and image journals."
)

trades = DataEngine.load_trades()
sync_status = DataEngine.load_sync_status()

section("Import Status")

if trades is None or trades.empty:
    stat_row([
        {
            "label": "Trades",
            "value": 0,
            "helper": "No trades loaded",
            "status": "warning",
        },
        {
            "label": "MT5 Sync",
            "value": "Waiting",
            "helper": "Desktop agent not connected",
            "status": "warning",
        },
    ])
else:
    stat_row([
        {
            "label": "Trades",
            "value": len(trades),
            "helper": "Loaded records",
            "status": "positive",
        },
        {
            "label": "Latest Trade",
            "value": trades.iloc[0].get("trade_date", "-"),
            "helper": "Most recent close",
            "status": "neutral",
        },
    ])

if sync_status is not None and not sync_status.empty:
    status = sync_status.iloc[0]

    stat_row([
        {
            "label": "Sync Status",
            "value": status.get("status", "-"),
            "helper": status.get("message", ""),
            "status": "positive" if status.get("status") == "connected" else "warning",
        },
        {
            "label": "Last Sync",
            "value": status.get("last_sync", "-"),
            "helper": "Desktop MT5 agent",
            "status": "neutral",
        },
    ])

section("MT5 Desktop Sync")

command_card(
    "Recommended Import Method",
    "Run the desktop sync agent on the same Windows computer as MT5. It will automatically sync account balance, open positions and closed trades.",
    "Use desktop_sync/sync_agent.py"
)

section("CSV Manual Import")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        preview = pd.read_csv(uploaded_file)

        table_header(
            "CSV Preview",
            "First 20 rows"
        )

        st.dataframe(
            preview.head(20),
            use_container_width=True,
            hide_index=True
        )

        st.warning(
            "CSV import mapping will be handled in the final production setup."
        )

    except Exception as error:
        st.error(f"Could not read CSV: {error}")

section("Screenshot Imports")

command_card(
    "Screenshot Watchers",
    "Use the desktop screenshot watcher to automatically upload TradingView and MT5 screenshots into TradeHub.",
    "Use desktop_sync/screenshot_watcher.py"
)

images = st.file_uploader(
    "Manual Screenshot Upload",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if images:
    st.info(
        f"{len(images)} image(s) selected. Manual upload connection will be completed in the final production setup."
    )
