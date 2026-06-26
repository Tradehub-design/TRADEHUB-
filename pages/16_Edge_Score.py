import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.edge_score import EdgeScoreEngine
from engine.grade import GradeEngine


load_css()

app_header(
    "⭐ Edge Score",
    "Measure execution quality instead of judging trades only by profit."
)

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using Edge Score.",
        "Go to Import."
    )
    st.stop()

if reviews is None or reviews.empty:
    command_card(
        "No trade reviews yet",
        "Complete trade reviews to generate Edge Scores.",
        "Go to Trade Review."
    )
    st.stop()

merged = trades.merge(
    reviews,
    left_on=["ticket", "account_number"],
    right_on=["trade_ticket", "account_number"],
    how="inner"
)

if merged.empty:
    command_card(
        "No linked reviews",
        "Your reviews need to match imported trades by ticket and account.",
        "Review one recent trade first."
    )
    st.stop()

rows = []

for _, row in merged.iterrows():
    trade = row.to_dict()
    review = row.to_dict()

    edge = EdgeScoreEngine.calculate(review, trade)
    grade = GradeEngine.grade(edge)

    rows.append({
        "ticket": row.get("ticket"),
        "symbol": row.get("symbol"),
        "direction": row.get("direction"),
        "net_profit": row.get("net_profit"),
        "trade_grade": row.get("trade_grade"),
        "rule_score": row.get("rule_score"),
        "confidence": row.get("confidence_score"),
        "mistake": row.get("mistake_type"),
        "edge_score": edge,
        "edge_grade": grade,
    })

scores = pd.DataFrame(rows)

section("Edge Overview")

average_edge = round(scores["edge_score"].mean(), 1)
best_edge = int(scores["edge_score"].max())
worst_edge = int(scores["edge_score"].min())

stat_row([
    {
        "label": "Average Edge",
        "value": average_edge,
        "helper": "All reviewed trades",
        "status": "positive" if average_edge >= 80 else "warning",
    },
    {
        "label": "Best Edge",
        "value": best_edge,
        "helper": GradeEngine.grade(best_edge),
        "status": "positive",
    },
    {
        "label": "Worst Edge",
        "value": worst_edge,
        "helper": GradeEngine.grade(worst_edge),
        "status": "negative",
    },
])

stat_row([
    {
        "label": "Reviewed Trades",
        "value": len(scores),
        "helper": "With journal review",
        "status": "neutral",
    },
    {
        "label": "A Grade+",
        "value": len(scores[scores["edge_score"] >= 80]),
        "helper": "Strong execution",
        "status": "positive",
    },
    {
        "label": "Weak Edge",
        "value": len(scores[scores["edge_score"] < 70]),
        "helper": "Needs review",
        "status": "negative",
    },
])

section("Edge Leaderboard")

table_header(
    "Trade Quality",
    "Sorted by execution quality, not just profit."
)

st.dataframe(
    scores.sort_values("edge_score", ascending=False),
    use_container_width=True,
    hide_index=True
)

section("Edge by Symbol")

symbol_edge = (
    scores.groupby("symbol")
    .agg(
        Trades=("symbol", "count"),
        AverageEdge=("edge_score", "mean"),
        NetProfit=("net_profit", "sum"),
    )
    .reset_index()
    .sort_values("AverageEdge", ascending=False)
)

symbol_edge["AverageEdge"] = symbol_edge["AverageEdge"].round(1)

st.dataframe(
    symbol_edge,
    use_container_width=True,
    hide_index=True
)

section("Edge by Mistake")

mistake_edge = (
    scores.groupby("mistake")
    .agg(
        Trades=("mistake", "count"),
        AverageEdge=("edge_score", "mean"),
        NetProfit=("net_profit", "sum"),
    )
    .reset_index()
    .sort_values("NetProfit", ascending=True)
)

mistake_edge["AverageEdge"] = mistake_edge["AverageEdge"].round(1)

st.dataframe(
    mistake_edge,
    use_container_width=True,
    hide_index=True
)
