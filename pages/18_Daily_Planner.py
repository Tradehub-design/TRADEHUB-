import streamlit as st
from datetime import date

from utils.supabase_client import get_supabase_client

from core.ui import load_css, app_header, section
from planner.planner_engine import PlannerEngine

load_css()

app_header(
    "📅 Daily Planner",
    "Plan your trading day before placing your first trade."
)

supabase = get_supabase_client()

today = date.today()

section("Market Bias")

pairs = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCAD",
    "AUDUSD",
    "NZDUSD",
    "XAUUSD"
]

market_bias = {}

cols = st.columns(2)

for i, pair in enumerate(pairs):

    with cols[i % 2]:

        market_bias[pair] = st.selectbox(
            pair,
            [
                "Bullish",
                "Bearish",
                "Neutral"
            ]
        )

section("Today's Focus")

focus = st.multiselect(
    "",
    [
        "Liquidity Sweep",
        "Continuation",
        "Weekly Zones",
        "Daily Zones",
        "FVG",
        "Breakout",
        "Reversal"
    ]
)

section("News")

news = st.multiselect(
    "",
    [
        "High Impact",
        "FOMC",
        "CPI",
        "NFP",
        "No Major News"
    ]
)

section("Risk")

col1, col2, col3 = st.columns(3)

with col1:
    max_risk = st.number_input(
        "Max Risk %",
        value=2.0
    )

with col2:
    max_trades = st.number_input(
        "Max Trades",
        value=3
    )

with col3:
    stop_after_losses = st.number_input(
        "Stop After Losses",
        value=2
    )

section("Psychology")

sleep = st.slider("Sleep", 1, 5, 4)

stress = st.slider("Stress", 1, 5, 2)

confidence = st.slider("Confidence", 1, 5, 4)

section("Today's Goals")

goals = st.multiselect(
    "",
    [
        "Wait for confirmation",
        "No revenge trading",
        "Follow playbook",
        "Journal every trade",
        "Respect max risk",
        "Only A+ setups"
    ]
)

notes = st.text_area(
    "Notes"
)

if st.button("Save Daily Plan"):

    payload = PlannerEngine.build_payload(
        today,
        market_bias,
        focus,
        news,
        max_risk,
        max_trades,
        stop_after_losses,
        sleep,
        stress,
        confidence,
        goals,
        notes
    )

    supabase.table("daily_plans").upsert(
        payload,
        on_conflict="plan_date"
    ).execute()

    st.success("Daily plan saved.")
