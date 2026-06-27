import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row
from data.data_engine import DataEngine
from core.ai_coach_engine import AICoachEngine
from engine.habit_engine import HabitEngine


load_css()

app_header(
    "🤖 AI Coach",
    "Personal coaching based on your trades, reviews and habits."
)

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()

if trades is None or trades.empty:
    command_card("No trades found", "Import trades first.", "Waiting for data.")
    st.stop()

if reviews is None:
    reviews = pd.DataFrame()

summary = AICoachEngine.generate_summary(trades, reviews)
habits = HabitEngine.detect(trades, reviews)

section("Coach Summary")

command_card(
    "Today’s Trading Insight",
    summary["main_message"],
    summary["suggested_focus"]
)

section("Performance Diagnosis")

stat_row([
    {"label": "Best Symbol", "value": summary["best_symbol"], "helper": "Highest profit", "status": "positive"},
    {"label": "Worst Symbol", "value": summary["worst_symbol"], "helper": "Lowest profit", "status": "negative"},
    {"label": "Best Session", "value": summary["best_session"], "helper": "Best window", "status": "positive"},
    {"label": "Worst Session", "value": summary["worst_session"], "helper": "Weakest window", "status": "negative"},
])

section("Detected Habits")

for habit in habits:
    command_card("Habit Detected", habit, "Rule-based coaching")

section("Ask TradeHub")

question = st.text_area("Question", placeholder="Example: What should I focus on next?")

if st.button("Analyse"):
    command_card(
        "Coach Response",
        "Your current focus should be reducing repeated mistakes and prioritising your strongest symbol/session combinations.",
        "Full AI model connection later."
    )
