import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row
from core.screenshot_engine import ScreenshotEngine


load_css()

app_header(
    "🖼️ Screenshot Journal",
    "Attach before, entry, exit and review screenshots to your trades."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

trade_response = (
    supabase.table("trades")
    .select("*")
    .order("trade_date", desc=True)
    .execute()
)

trades_df = prepare_trades_dataframe(trade_response.data)

if trades_df.empty:
    command_card(
        "No trades found",
        "Import trades before adding screenshots.",
        "Go to Import."
    )
    st.stop()

section("Select Trade")

trade_options = []

for _, trade in trades_df.iterrows():
    label = f"{trade.get('ticket')} | {trade.get('symbol')} | {trade.get('direction')} | {trade.get('net_profit')}"
    trade_options.append((label, trade.to_dict()))

selected_label = st.selectbox(
    "Trade",
    [item[0] for item in trade_options]
)

selected_trade = next(
    item[1] for item in trade_options
    if item[0] == selected_label
)

ticket = selected_trade.get("ticket")
account_number = selected_trade.get("account_number")

stat_row([
    {
        "label": "Symbol",
        "value": selected_trade.get("symbol", "-"),
        "helper": "Instrument",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": selected_trade.get("net_profit", 0),
        "helper": "Closed result",
        "status": "positive" if selected_trade.get("net_profit", 0) >= 0 else "negative",
    },
])

st.divider()

section("Upload Screenshot")

screenshot_type = st.selectbox(
    "Screenshot Type",
    [
        "Before Entry",
        "Entry",
        "Exit",
        "After Trade",
        "Review",
        "Mistake",
        "Other",
    ]
)

uploaded_file = st.file_uploader(
    "Upload screenshot",
    type=["png", "jpg", "jpeg"]
)

notes = st.text_area(
    "Screenshot Notes",
    placeholder="What does this screenshot show?"
)

if st.button("Upload Screenshot"):
    if uploaded_file is None:
        st.error("Please upload a screenshot first.")
    else:
        file_path = ScreenshotEngine.build_file_path(
            ticket,
            account_number,
            screenshot_type,
            uploaded_file.name
        )

        file_bytes = uploaded_file.getvalue()

        supabase.storage.from_("trade-screenshots").upload(
            file_path,
            file_bytes,
            {
                "content-type": uploaded_file.type,
                "upsert": "true",
            }
        )

        public_url = supabase.storage.from_("trade-screenshots").get_public_url(
            file_path
        )

        payload = ScreenshotEngine.create_payload(
            ticket,
            account_number,
            screenshot_type,
            file_path,
            public_url,
            notes
        )

        supabase.table("trade_screenshots").insert(payload).execute()

        st.success("Screenshot uploaded successfully.")

st.divider()

section("Screenshots for This Trade")

shot_response = (
    supabase.table("trade_screenshots")
    .select("*")
    .eq("trade_ticket", ticket)
    .eq("account_number", account_number)
    .order("created_at", desc=True)
    .execute()
)

screenshots = shot_response.data

if not screenshots:
    command_card(
        "No screenshots yet",
        "Upload before/after screenshots to build a visual trading journal.",
        "This will later power AI trade review."
    )
else:
    for shot in screenshots:
        st.markdown(f"### {shot.get('screenshot_type')}")
        st.image(shot.get("public_url"), use_container_width=True)

        if shot.get("notes"):
            st.info(shot.get("notes"))

        st.caption(shot.get("created_at"))
        st.divider()
