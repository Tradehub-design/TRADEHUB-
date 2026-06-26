import streamlit as st
from datetime import date

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row
from utils.supabase_client import get_supabase_client
from planner.planner_engine import PlannerEngine


load_css()

app_header(
    "📅 Daily Planner",
    "Plan your trading day before placing the first trade."
)

supabase = get_supabase_client()
today = date.today()

section("Today")

stat_row([
    {
        "label": "Plan Date",
        "value": str(today),
        "helper": "Trading day",
        "status": "neutral",
    },
    {
        "label": "Planning Status",
        "value": "Active",
        "helper": "Prepare before trading",
        "status": "positive",
    },
    {
        "label": "Rule",
        "value": "Plan First",
        "helper": "No plan, no trade",
        "status": "warning",
    },
])

section("Market Bias")

pairs = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCAD",
    "AUDUSD",
    "NZDUSD",
    "XAUUSD",
    "GBPJPY",
    "EURJPY",
]

market_bias = {}

cols = st.columns(3)

for i, pair in enumerate(pairs):
    with cols[i % 3]:
        market_bias[pair] = st.selectbox(
            pair,
            ["Bullish", "Bearish", "Neutral"],
        )

section("Trading Focus")

focus = st.multiselect(
    "Focus Areas",
    [
        "Liquidity Sweep",
        "Continuation",
        "Weekly Zones",
        "Daily Zones",
        "FVG",
        "Breakout",
        "Reversal",
        "London Open",
        "New York Open",
        "No Trade Day",
    ],
)

news = st.multiselect(
    "News Conditions",
    [
        "High Impact",
        "FOMC",
        "CPI",
        "NFP",
        "Interest Rate",
        "No Major News",
    ],
)

section("Risk Rules")

col1, col2, col3 = st.columns(3)

with col1:
    max_risk = st.number_input(
        "Max Risk %",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1,
    )

with col2:
    max_trades = st.number_input(
        "Max Trades",
        min_value=0,
        max_value=20,
        value=3,
        step=1,
    )

with col3:
    stop_after_losses = st.number_input(
        "Stop After Losses",
        min_value=0,
        max_value=10,
        value=2,
        step=1,
    )

section("Psychology Check")

sleep = st.slider("Sleep", 1, 5, 4)
stress = st.slider("Stress", 1, 5, 2)
confidence = st.slider("Confidence", 1, 5, 4)

stat_row([
    {
        "label": "Sleep",
        "value": sleep,
        "helper": "1 poor / 5 strong",
        "status": "positive" if sleep >= 4 else "warning",
    },
    {
        "label": "Stress",
        "value": stress,
        "helper": "Lower is better",
        "status": "positive" if stress <= 2 else "warning",
    },
    {
        "label": "Confidence",
        "value": confidence,
        "helper": "Trading readiness",
        "status": "positive" if confidence >= 4 else "warning",
    },
])

section("Today's Goals")

goals = st.multiselect(
    "Goals",
    [
        "Wait for confirmation",
        "No revenge trading",
        "Follow playbook",
        "Journal every trade",
        "Respect max risk",
        "Only A+ setups",
        "Stop after rules are broken",
    ],
)

notes = st.text_area(
    "Notes",
    placeholder="What should you remember today?"
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
        notes,
    )

    supabase.table("daily_plans").upsert(
        payload,
        on_conflict="plan_date",
    ).execute()

    st.cache_data.clear()
    st.success("Daily plan saved.")

section("Plan Summary")

command_card(
    "Today's Trading Rules",
    f"Maximum {max_trades} trades, maximum {max_risk}% risk, stop after {stop_after_losses} losses.",
    "Follow this plan before taking any trade.",
)
