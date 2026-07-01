import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, trade_quality_card
from data.data_engine import DataEngine
from utils.supabase_client import get_supabase_client
from core.journal_engine import JournalEngine


load_css()

app_header(
    "📔 Trade Review",
    "Review execution, discipline, emotion, mistakes and lessons for each trade."
)

supabase = get_supabase_client()

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()

playbook_response = (
    supabase.table("playbooks")
    .select("*")
    .order("created_at", desc=True)
    .execute()
)

playbooks = playbook_response.data or []

if trades is None or trades.empty:
    command_card(
        "No trades available",
        "Import trades before creating reviews.",
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
net_profit = selected_trade.get("net_profit") or 0

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
        "value": net_profit,
        "helper": "Closed result",
        "status": "positive" if net_profit >= 0 else "negative",
    },
    {
        "label": "Session",
        "value": selected_trade.get("session", "-"),
        "helper": "Trading session",
        "status": "neutral",
    },
])

existing_review = None

if reviews is not None and not reviews.empty:
    review_match = reviews[
        (reviews["trade_ticket"] == ticket)
        & (reviews["account_number"] == account_number)
    ]

    if not review_match.empty:
        existing_review = review_match.iloc[0].to_dict()

section("Review Form")

playbook_options = {"None": None}

for playbook in playbooks:
    playbook_options[playbook["name"]] = playbook["id"]

with st.form("trade_review_form"):
    playbook_name = st.selectbox(
        "Playbook Used",
        list(playbook_options.keys())
    )

    playbook_id = playbook_options[playbook_name]

    col1, col2 = st.columns(2)

    with col1:
        total_rules = st.number_input(
            "Total Rules",
            min_value=0,
            value=int(existing_review.get("total_rules", 5)) if existing_review else 5,
            step=1
        )

        rules_followed = st.number_input(
            "Rules Followed",
            min_value=0,
            value=int(existing_review.get("rules_followed", 5)) if existing_review else 5,
            step=1
        )

    with col2:
        confidence_score = st.slider(
            "Confidence Score",
            0,
            10,
            int(existing_review.get("confidence_score", 7)) if existing_review else 7
        )

        mistake_type = st.selectbox(
            "Mistake Type",
            [
                "None",
                "Entered Early",
                "Entered Late",
                "Against Bias",
                "Overtrading",
                "Moved Stop Loss",
                "Closed Too Early",
                "Held Too Long",
                "Revenge Trade",
                "No Confirmation",
                "Wrong Session",
                "Other",
            ]
        )

    emotion_before = st.selectbox(
        "Emotion Before Trade",
        [
            "Calm",
            "Confident",
            "Neutral",
            "FOMO",
            "Frustrated",
            "Tired",
            "Revenge",
            "Anxious",
        ]
    )

    emotion_after = st.selectbox(
        "Emotion After Trade",
        [
            "Calm",
            "Happy",
            "Neutral",
            "Frustrated",
            "Regretful",
            "Overconfident",
            "Anxious",
        ]
    )

    lesson_learned = st.text_area(
        "Lesson Learned",
        value=existing_review.get("lesson_learned", "") if existing_review else "",
        placeholder="What did this trade teach you?"
    )

    journal_notes = st.text_area(
        "Journal Notes",
        value=existing_review.get("journal_notes", "") if existing_review else "",
        placeholder="Describe the setup, entry, exit and thought process."
    )

    submitted = st.form_submit_button("Save Review")

    if submitted:
        if rules_followed > total_rules:
            st.error("Rules followed cannot be greater than total rules.")
        else:
            payload = JournalEngine.create_review_payload(
                ticket,
                account_number,
                playbook_id,
                rules_followed,
                total_rules,
                confidence_score,
                emotion_before,
                emotion_after,
                mistake_type,
                lesson_learned,
                journal_notes
            )

            supabase.table("trade_journal_reviews").upsert(
                payload,
                on_conflict="trade_ticket,account_number"
            ).execute()

            st.cache_data.clear()
            st.success("Trade review saved.")
            st.rerun()

section("Existing Review")

if not existing_review:
    command_card(
        "No review yet",
        "Complete the form above to create a structured trade review.",
        "This powers Edge Score, Research and AI Coach."
    )
else:
    trade_quality_card(
        int(existing_review.get("rule_score") or 0),
        f"Grade: {existing_review.get('trade_grade')} | Confidence: {existing_review.get('confidence_score')}/10"
    )

    stat_row([
        {
            "label": "Rules Followed",
            "value": f"{existing_review.get('rules_followed')}/{existing_review.get('total_rules')}",
            "helper": "Checklist discipline",
            "status": "positive" if existing_review.get("rule_score", 0) >= 80 else "negative",
        },
        {
            "label": "Mistake",
            "value": existing_review.get("mistake_type"),
            "helper": "Recorded issue",
            "status": "neutral" if existing_review.get("mistake_type") == "None" else "negative",
        },
        {
            "label": "Emotion Before",
            "value": existing_review.get("emotion_before"),
            "helper": "Psychology",
            "status": "neutral",
        },
    ])

    command_card(
        "🤖 AI Review Preview",
        JournalEngine.ai_style_summary(existing_review),
        "Full AI review later."
    )

    command_card(
        "Lesson Learned",
        existing_review.get("lesson_learned") or "No lesson recorded.",
        "Journal"
    )

    command_card(
        "Journal Notes",
        existing_review.get("journal_notes") or "No notes recorded.",
        "Journal"
    )
