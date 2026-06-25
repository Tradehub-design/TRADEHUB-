import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe
from core.ui import load_css, app_header, section
from core.components import command_card, stat_row
from core.ai_coach_engine import AICoachEngine

load_css()

app_header(
    "🤖 AI Coach",
    "Your personal trading coach powered by your trades, journal reviews and playbook discipline."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

trade_response = supabase.table("trades").select("*").execute()
review_response = supabase.table("trade_journal_reviews").select("*").execute()

df = prepare_trades_dataframe(trade_response.data)
reviews = pd.DataFrame(review_response.data)

if df.empty:
    command_card(
        "No trades found",
        "Import trades first so your AI Coach can analyse your performance.",
        "The more trades you journal, the smarter this page becomes."
    )
    st.stop()

summary = AICoachEngine.generate_summary(df, reviews)

section("Coach Summary")

command_card(
    "Today’s Trading Insight",
    summary["main_message"],
    summary["suggested_focus"]
)

section("Performance Diagnosis")

stat_row([
    {"label": "Best Symbol", "value": summary["best_symbol"], "helper": "Highest net profit", "status": "positive"},
    {"label": "Worst Symbol", "value": summary["worst_symbol"], "helper": "Lowest net profit", "status": "negative"},
])

stat_row([
    {"label": "Best Session", "value": summary["best_session"], "helper": "Highest net profit", "status": "positive"},
    {"label": "Worst Session", "value": summary["worst_session"], "helper": "Lowest net profit", "status": "negative"},
])

section("Discipline & Mistakes")

stat_row([
    {
        "label": "Discipline Score",
        "value": f"{summary['discipline_score']}%",
        "helper": "Average journal rule score",
        "status": "positive" if summary["discipline_score"] >= 80 else "negative",
    },
    {
        "label": "Most Common Mistake",
        "value": summary["most_common_mistake"],
        "helper": "From trade reviews",
        "status": "negative",
    },
])

section("Ask TradeHub")

question = st.text_area(
    "Ask a question",
    placeholder="Example: What am I doing wrong? Which symbol should I avoid?"
)

if st.button("Analyse"):
    command_card(
        "AI Coach Response",
        "Full AI analysis will be connected later. For now, use the diagnosis above as your coaching summary.",
        "Next version will use your journal, playbooks and trade history together."
    )
