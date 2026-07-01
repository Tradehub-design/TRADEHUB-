import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header, trade_quality_card
from data.data_engine import DataEngine
from engine.edge_score import EdgeScoreEngine
from engine.grade import GradeEngine
from replay.replay_engine import ReplayEngine
from utils.supabase_client import get_supabase_client


load_css()

app_header(
    "🎬 Trade Replay",
    "Review the full story of each trade: result, execution, screenshots and lessons."
)

supabase = get_supabase_client()

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()
screenshots = DataEngine.load_screenshots()
replays = DataEngine.load_replays()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using Trade Replay.",
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

section("Trade Summary")

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

review_row = pd.DataFrame()

if reviews is not None and not reviews.empty:
    review_row = reviews[
        (reviews["trade_ticket"] == ticket)
        & (reviews["account_number"] == account_number)
    ]

if not review_row.empty:
    review = review_row.iloc[0].to_dict()

    edge = EdgeScoreEngine.calculate(
        review,
        selected_trade
    )

    grade = GradeEngine.grade(edge)

    section("Execution Quality")

    col1, col2 = st.columns([0.8, 1.2])

    with col1:
        trade_quality_card(
            edge,
            f"Grade {grade}"
        )

    with col2:
        stat_row([
            {
                "label": "Rule Score",
                "value": review.get("rule_score", "-"),
                "helper": "Discipline",
                "status": "positive" if review.get("rule_score", 0) >= 80 else "warning",
            },
            {
                "label": "Confidence",
                "value": review.get("confidence_score", "-"),
                "helper": "Self-rated",
                "status": "neutral",
            },
        ])

        stat_row([
            {
                "label": "Mistake",
                "value": review.get("mistake_type", "-"),
                "helper": "Recorded issue",
                "status": "negative" if review.get("mistake_type") not in [None, "None", "-"] else "neutral",
            },
            {
                "label": "Emotion",
                "value": review.get("emotion_before", "-"),
                "helper": "Before trade",
                "status": "neutral",
            },
        ])

    section("Journal")

    command_card(
        "Lesson Learned",
        review.get("lesson_learned") or "No lesson recorded.",
        "From Trade Review"
    )

    command_card(
        "Journal Notes",
        review.get("journal_notes") or "No journal notes recorded.",
        "From Trade Review"
    )
else:
    command_card(
        "No trade review yet",
        "Complete a Trade Review to activate Edge Score and journal insights.",
        "Go to Trade Review."
    )

section("Screenshot Timeline")

trade_shots = pd.DataFrame()

if screenshots is not None and not screenshots.empty:
    trade_shots = screenshots[
        (screenshots["trade_ticket"] == ticket)
        & (screenshots["account_number"] == account_number)
    ]

if trade_shots.empty:
    command_card(
        "No screenshots yet",
        "Upload screenshots to build a visual trade timeline.",
        "Go to Screenshot Journal."
    )
else:
    table_header(
        "Visual Timeline",
        f"{len(trade_shots)} screenshots attached"
    )

    for _, shot in trade_shots.iterrows():
        st.markdown(f"### {shot.get('screenshot_type', 'Screenshot')}")
        st.image(
            shot.get("public_url"),
            use_container_width=True
        )

        if shot.get("notes"):
            st.info(shot.get("notes"))

        st.caption(shot.get("created_at"))

section("Replay Notes")

existing_replay = pd.DataFrame()

if replays is not None and not replays.empty:
    existing_replay = replays[
        (replays["trade_ticket"] == ticket)
        & (replays["account_number"] == account_number)
    ]

default_summary = ""
default_lessons = ""
default_improvements = ""

if not existing_replay.empty:
    replay_row = existing_replay.iloc[0]
    default_summary = replay_row.get("summary") or ""
    default_lessons = replay_row.get("lessons") or ""
    default_improvements = replay_row.get("improvements") or ""

summary = st.text_area(
    "Summary",
    value=default_summary
)

lessons = st.text_area(
    "Lessons Learned",
    value=default_lessons
)

improvements = st.text_area(
    "What will you improve next time?",
    value=default_improvements
)

if st.button("Save Replay"):
    payload = ReplayEngine.build_payload(
        ticket,
        account_number,
        summary,
        lessons,
        improvements
    )

    supabase.table("trade_replays").upsert(
        payload,
        on_conflict="trade_ticket"
    ).execute()

    st.cache_data.clear()
    st.success("Replay saved.")
    st.rerun()
