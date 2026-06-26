import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine


load_css()

app_header(
    "📥 Import Centre",
    "Import MT5 history and prepare TradeHub for automatic sync."
)

section("Current Data")

existing_trades = DataEngine.load_trades()

if existing_trades is None or existing_trades.empty:
    stat_row([
        {
            "label": "Imported Trades",
            "value": 0,
            "helper": "No trades yet",
            "status": "neutral",
        },
        {
            "label": "Status",
            "value": "Waiting",
            "helper": "Upload your MT5 export",
            "status": "warning",
        },
    ])
else:
    stat_row([
        {
            "label": "Imported Trades",
            "value": len(existing_trades),
            "helper": "Stored in Supabase",
            "status": "positive",
        },
        {
            "label": "Latest Trade",
            "value": existing_trades.iloc[0].get("trade_date", "-"),
            "helper": "Most recent record",
            "status": "neutral",
        },
    ])

section("Manual Import")

command_card(
    "MT5 Manual Import",
    "Upload your exported MT5 trade history file here. Automatic MT5 Sync will later replace this manual process.",
    "Accepted format: CSV-style trade history."
)

uploaded_file = st.file_uploader(
    "Upload trade history CSV",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        preview = pd.read_csv(uploaded_file)

        table_header(
            "Preview",
            "Check the uploaded file before importing."
        )

        st.dataframe(
            preview.head(20),
            use_container_width=True,
            hide_index=True
        )

        if st.button("Import Previewed File"):
            st.warning(
                "Importer mapping is currently handled by your existing import workflow."
            )

    except Exception as e:
        st.error(f"Unable to read file: {e}")

section("Automatic Sync Status")

command_card(
    "MT5 Sync Agent",
    "Not connected yet. Once your Windows computer is available, the sync agent will upload trades directly to Supabase.",
    "Your app is already structured for automatic sync."
)
