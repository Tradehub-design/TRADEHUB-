import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from core.screenshot_engine import ScreenshotEngine
from utils.supabase_client import get_supabase_client


load_css()

app_header(
    "🖼️ Screenshot Journal",
    "Create a visual trade timeline: before, entry, management, exit and review."
)

supabase = get_supabase_client()

trades = DataEngine.load_trades()
screenshots = DataEngine.load_screenshots()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before adding screenshots.",
        "Go to Import."
    )
    st.stop()

section("Select Trade")

trade_options = []

for _, trade in trades.iterrows():
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

section("Trade Snapshot")

stat_row([
    {
        "label": "Symbol",
        "value": selected_trade.get("symbol", "-"),
        "helper": "Instrument",
        "status": "neutral",
    },
    {
        "label": "Direction",
        "value": selected_trade.get("direction", "-"),
        "helper": "Buy / Sell",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": selected_trade.get("net_profit", 0),
        "helper": "Closed result",
        "status": "positive" if selected_trade.get("net_profit", 0) >= 0 else "negative",
    },
    {
        "label": "Session",
        "value": selected_trade.get("session", "-"),
        "helper": "Trading session",
        "status": "neutral",
    },
])

screenshot_slots = [
    "Before Entry",
    "Entry",
    "Trade Management",
    "Exit",
    "After Trade",
    "Higher Timeframe",
    "Lower Timeframe",
    "Review",
    "Mistake",
    "Other",
]

section("Upload Screenshot")

selected_slot = st.selectbox(
    "Screenshot Slot",
    screenshot_slots
)

uploaded_file = st.file_uploader(
    "Upload screenshot",
    type=["png", "jpg", "jpeg"],
    key=f"uploader_{ticket}_{selected_slot}"
)

notes = st.text_area(
    "Screenshot Notes",
    placeholder="What does this screenshot show?",
    key=f"notes_{ticket}_{selected_slot}"
)

if st.button("Upload Screenshot"):
    if uploaded_file is None:
        st.error("Please upload a screenshot first.")
    else:
        file_path = ScreenshotEngine.build_file_path(
            ticket,
            account_number,
            selected_slot,
            uploaded_file.name
        )

        supabase.storage.from_("trade-screenshots").upload(
            file_path,
            uploaded_file.getvalue(),
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
            selected_slot,
            file_path,
            public_url,
            notes
        )

        supabase.table("trade_screenshots").insert(payload).execute()

        st.success("Screenshot uploaded successfully.")
        st.cache_data.clear()
        st.rerun()

section("Visual Timeline")

if screenshots is None or screenshots.empty:
    command_card(
        "No screenshots yet",
        "Upload before, entry and exit screenshots to build your visual journal.",
        "Start with Before Entry."
    )
else:
    screenshot_df = screenshots[
        (screenshots["trade_ticket"] == ticket)
        & (screenshots["account_number"] == account_number)
    ]

    if screenshot_df.empty:
        command_card(
            "No screenshots for this trade",
            "Upload screenshots into the slots above.",
            "Recommended: Before Entry, Entry, Exit."
        )
    else:
        stat_row([
            {
                "label": "Screenshots",
                "value": len(screenshot_df),
                "helper": "Attached to this trade",
                "status": "positive",
            },
            {
                "label": "Slots Used",
                "value": screenshot_df["screenshot_type"].nunique(),
                "helper": "Timeline coverage",
                "status": "neutral",
            },
        ])

        for slot in screenshot_slots:
            slot_images = screenshot_df[
                screenshot_df["screenshot_type"] == slot
            ]

            with st.expander(
                f"{slot} ({len(slot_images)})",
                expanded=len(slot_images) > 0
            ):
                if slot_images.empty:
                    st.info(f"No {slot} screenshot uploaded yet.")
                else:
                    table_header(
                        slot,
                        f"{len(slot_images)} screenshot(s)"
                    )

                    for _, shot in slot_images.iterrows():
                        st.image(
                            shot.get("public_url"),
                            use_container_width=True
                        )

                        if shot.get("notes"):
                            st.info(shot.get("notes"))

                        st.caption(shot.get("created_at"))
