import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.screenshot_link_engine import ScreenshotLinkEngine
from components.screenshot_timeline import ScreenshotTimeline


load_css()

app_header(
    "▶ Replay Centre",
    "Replay the full story of every trade using trade data, screenshots and review context."
)

trades = DataEngine.load_trades()
screenshots = DataEngine.load_screenshots()
reviews = DataEngine.load_reviews()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades first.",
        "Replay needs trade history."
    )
    st.stop()

trade_options = []

for _, trade in trades.iterrows():
    label = f"{trade.get('ticket')} | {trade.get('symbol')} | {trade.get('direction')} | {trade.get('net_profit')}"
    trade_options.append((label, trade.to_dict()))

selected_label = st.selectbox(
    "Select Trade",
    [item[0] for item in trade_options]
)

selected_trade = next(
    item[1] for item in trade_options
    if item[0] == selected_label
)

ticket = selected_trade.get("ticket")
account_number = selected_trade.get("account_number")

linked_screenshots = ScreenshotLinkEngine.screenshots_for_trade(
    screenshots,
    ticket,
    account_number
)

review = None

 if reviews is not None and not reviews.empty:
    matched_reviews = reviews[
        (reviews["trade_ticket"].astype(str) == str(ticket))
        & (reviews["account_number"].astype(str) == str(account_number))
    ] if "trade_ticket" in reviews.columns and "account_number" in reviews.columns else reviews.iloc[0:0]

    if not matched_reviews.empty:
        review = matched_reviews.iloc[0].to_dict()

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
        "label": "Screenshots",
        "value": len(linked_screenshots) if linked_screenshots is not None else 0,
        "helper": "Linked images",
        "status": "positive" if linked_screenshots is not None and not linked_screenshots.empty else "warning",
    },
])

section("Trade Timeline")

timeline = [
    {
        "Stage": "Open",
        "Time": selected_trade.get("open_time", "-"),
        "Status": "Completed",
    },
    {
        "Stage": "Close",
        "Time": selected_trade.get("trade_date", "-"),
        "Status": "Completed",
    },
]

if review:
    timeline.append({
        "Stage": "Review",
        "Time": review.get("created_at", "-"),
        "Status": "Completed",
    })

table_header(
    "Timeline",
    "Trade open, screenshots, close and review."
)

st.dataframe(
    timeline,
    use_container_width=True,
    hide_index=True
)

section("Screenshots")

ScreenshotTimeline.render(
    linked_screenshots
)

section("Review Notes")

if review:
    command_card(
        "Lesson Learned",
        review.get("lesson_learned") or "No lesson recorded.",
        "Trade Review"
    )

    command_card(
        "Journal Notes",
        review.get("journal_notes") or "No journal notes recorded.",
        "Trade Review"
    )
else:
    command_card(
        "No review yet",
        "Complete a Trade Review to add lessons and journal notes.",
        "Trade Review"
    )
