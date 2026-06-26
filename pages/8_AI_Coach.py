import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row
from data.data_engine import DataEngine
from core.ai_coach_engine import AICoachEngine


load_css()

app_header(
    "🤖 AI Coach",
    "Rule-based coaching from your trades, journal reviews and discipline data."
)

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades first so your coach can analyse your performance.",
        "The more data you add, the smarter this becomes."
    )
    st.stop()

if reviews is None:
    reviews = pd.DataFrame()

summary = AICoachEngine.generate_summary(
    trades,
    reviews
)

section("Coach Summary")

command_card(
    "Today’s Trading Insight",
    summary["main_message"],
    summary["suggested_focus"]
)

section("Performance Diagnosis")

stat_row([
    {
        "label": "Best Symbol",
        "value": summary["best_symbol"],
        "helper": "Highest net profit",
        "status": "positive",
    },
    {
        "label": "Worst Symbol",
        "value": summary["worst_symbol"],
        "helper": "Lowest net profit",
        "status": "negative",
    },
    {
        "label": "Discipline Score",
        "value": f"{summary['discipline_score']}%",
        "helper": "Average journal score",
        "status": "positive" if summary["discipline_score"] >= 80 else "warning",
    },
])

stat_row([
    {
        "label": "Best Session",
        "value": summary["best_session"],
        "helper": "Highest net profit",
        "status": "positive",
    },
    {
        "label": "Worst Session",
        "value": summary["worst_session"],
        "helper": "Lowest net profit",
        "status": "negative",
    },
    {
        "label": "Most Common Mistake",
        "value": summary["most_common_mistake"],
        "helper": "From reviews",
        "status": "negative",
    },
])

section("Coach Notes")

command_card(
    "What TradeHub Sees",
    "Your current coaching summary is based on imported trades and completed trade reviews. Complete more reviews to improve the quality of the feedback.",
    "Screenshot and AI chart review will be connected later."
)

section("Ask TradeHub")

question = st.text_area(
    "Question",
    placeholder="Example: What am I doing wrong? Which symbol should I avoid?"
)

if st.button("Analyse"):
    command_card(
        "AI Coach Response",
        "Full AI analysis will be connected later. For now, use the diagnosis above as your coaching summary.",
        "Next stage will use your journal, playbooks and screenshots together."
    )
