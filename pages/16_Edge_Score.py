import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card

from engine.edge_score import EdgeScoreEngine
from engine.grade import GradeEngine

load_css()

app_header(
    "⭐ Edge Score",
    "Measure execution quality instead of just profitability."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

trade_response = (
    supabase.table("trades")
    .select("*")
    .order("trade_date", desc=True)
    .execute()
)

review_response = (
    supabase.table("trade_journal_reviews")
    .select("*")
    .execute()
)

trades = prepare_trades_dataframe(trade_response.data)
reviews = pd.DataFrame(review_response.data)

if trades.empty:
    command_card(
        "No trades",
        "Import trades before using Edge Score.",
        "Go to Import."
    )
    st.stop()

if reviews.empty:
    command_card(
        "No reviews",
        "Complete trade reviews first.",
        "Journal → Trade Review"
    )
    st.stop()

merged = trades.merge(
    reviews,
    left_on=["ticket","account_number"],
    right_on=["trade_ticket","account_number"],
    how="inner"
)

scores = []

for _, row in merged.iterrows():

    trade = row.to_dict()
    review = row.to_dict()

    edge = EdgeScoreEngine.calculate(
        review,
        trade
    )

    grade = GradeEngine.grade(edge)

    scores.append({
        "Ticket": row["ticket"],
        "Symbol": row["symbol"],
        "Net Profit": row["net_profit"],
        "Edge Score": edge,
        "Grade": grade
    })

scores_df = pd.DataFrame(scores)

section("Summary")

stat_row([
    {
        "label":"Average Edge",
        "value":round(scores_df["Edge Score"].mean(),1),
        "helper":"All reviewed trades",
        "status":"positive"
    },
    {
        "label":"Best Score",
        "value":scores_df["Edge Score"].max(),
        "helper":"Highest quality trade",
        "status":"positive"
    },
])

stat_row([
    {
        "label":"Lowest Score",
        "value":scores_df["Edge Score"].min(),
        "helper":"Needs improvement",
        "status":"negative"
    },
    {
        "label":"Trades",
        "value":len(scores_df),
        "helper":"Reviewed",
        "status":"neutral"
    },
])

section("All Edge Scores")

st.dataframe(
    scores_df.sort_values(
        "Edge Score",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)
