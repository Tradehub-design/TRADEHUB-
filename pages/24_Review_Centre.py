import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.review_intelligence_engine import ReviewIntelligenceEngine


load_css()

app_header(
    "🧠 Review Centre",
    "Study discipline, confidence, emotions and repeated mistakes."
)

reviews = DataEngine.load_reviews()

if reviews is None or reviews.empty:
    command_card(
        "No reviews yet",
        "Complete trade reviews to unlock review intelligence.",
        "Go to Trade Review."
    )
    st.stop()

summary = ReviewIntelligenceEngine.summary(reviews)

section("Review Summary")

stat_row([
    {"label": "Reviews", "value": summary["review_count"], "helper": "Completed reviews", "status": "neutral"},
    {"label": "Avg Rule Score", "value": f"{summary['average_rule_score']}%", "helper": "Discipline", "status": "positive" if summary["average_rule_score"] >= 80 else "warning"},
    {"label": "Avg Confidence", "value": summary["average_confidence"], "helper": "Self-rated", "status": "neutral"},
    {"label": "Common Mistake", "value": summary["most_common_mistake"], "helper": "Repeated issue", "status": "negative"},
])

section("Review Records")

table_header("Journal Reviews", "All completed trade reviews")

st.dataframe(
    reviews,
    use_container_width=True,
    hide_index=True
)
