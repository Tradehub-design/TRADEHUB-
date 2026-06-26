import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, summary_stats

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card

from core.ai_coach_engine import AICoachEngine
from engine.edge_score import EdgeScoreEngine
from engine.grade import GradeEngine
from engine.streak_engine import StreakEngine


load_css()

app_header(
    "🏠 Command Centre",
    "Your daily trading cockpit — performance, risk, edge score and coaching insight."
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

df = prepare_trades_dataframe(trade_response.data)
reviews = pd.DataFrame(review_response.data)

if df.empty:
    command_card(
        "No trades found",
        "Import trades to activate your Command Centre.",
        "Next step: go to Import."
    )
    st.stop()

stats = summary_stats(df)
coach = AICoachEngine.generate_summary(df, reviews)

section("Performance Snapshot")

stat_row([
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "All imported trades",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": stats["net_profit"],
        "helper": "Realised result",
        "status": "positive" if stats["net_profit"] >= 0 else "negative",
    },
])

stat_row([
    {
        "label": "Winning Trades",
        "value": stats["wins"],
        "helper": "Closed in profit",
        "status": "positive",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Wins / total trades",
        "status": "neutral",
    },
])

section("Trading Quality")

if not reviews.empty:
    merged = df.merge(
        reviews,
        left_on=["ticket", "account_number"],
        right_on=["trade_ticket", "account_number"],
        how="inner"
    )

    edge_scores = []

    for _, row in merged.iterrows():
        trade = row.to_dict()
        review = row.to_dict()
        edge_scores.append(EdgeScoreEngine.calculate(review, trade))

    if edge_scores:
        avg_edge = round(sum(edge_scores) / len(edge_scores), 1)
        best_edge = max(edge_scores)
        low_edge = min(edge_scores)

        stat_row([
            {
                "label": "Average Edge",
                "value": avg_edge,
                "helper": "Execution quality",
                "status": "positive" if avg_edge >= 75 else "negative",
            },
            {
                "label": "Best Edge",
                "value": best_edge,
                "helper": GradeEngine.grade(best_edge),
                "status": "positive",
            },
        ])

        stat_row([
            {
                "label": "Lowest Edge",
                "value": low_edge,
                "helper": GradeEngine.grade(low_edge),
                "status": "negative",
            },
            {
                "label": "Reviewed Trades",
                "value": len(edge_scores),
                "helper": "Journal completed",
                "status": "neutral",
            },
        ])
    else:
        command_card(
            "No reviewed trades yet",
            "Complete trade reviews to activate Edge Score.",
            "Go to Trade Review."
        )
else:
    command_card(
        "No journal reviews yet",
        "Review your trades to unlock Edge Score and discipline tracking.",
        "Go to Trade Review."
    )

section("Streaks")

streaks = StreakEngine.calculate(df.sort_values("trade_date"))

stat_row([
    {
        "label": "Current Win Streak",
        "value": streaks["current"],
        "helper": "Consecutive wins",
        "status": "positive",
    },
    {
        "label": "Best Win Streak",
        "value": streaks["best"],
        "helper": "Highest streak",
        "status": "positive",
    },
])

section("AI Coach")

command_card(
    "🤖 Today’s Focus",
    coach["main_message"],
    coach["suggested_focus"]
)

stat_row([
    {
        "label": "Best Symbol",
        "value": coach["best_symbol"],
        "helper": "Highest net profit",
        "status": "positive",
    },
    {
        "label": "Worst Symbol",
        "value": coach["worst_symbol"],
        "helper": "Lowest net profit",
        "status": "negative",
    },
])

stat_row([
    {
        "label": "Discipline Score",
        "value": f"{coach['discipline_score']}%",
        "helper": "Average rule score",
        "status": "positive" if coach["discipline_score"] >= 80 else "negative",
    },
    {
        "label": "Most Common Mistake",
        "value": coach["most_common_mistake"],
        "helper": "From journal reviews",
        "status": "negative",
    },
])

section("Recent Trades")

recent_cols = [
    col for col in [
        "ticket",
        "symbol",
        "direction",
        "net_profit",
        "trade_date",
        "session",
    ]
    if col in df.columns
]

st.dataframe(
    df[recent_cols].head(10),
    use_container_width=True,
    hide_index=True
)
