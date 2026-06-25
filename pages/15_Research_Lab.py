import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe
from core.ui import load_css, app_header, section
from core.components import stat_row, command_card
from research.queries import ResearchQueries
from research.insights import ResearchInsights

load_css()

app_header(
    "🔬 Research Lab",
    "Filter, compare and study your trading history to find what is actually working."
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

if not reviews.empty:
    df = df.merge(
        reviews,
        left_on=["ticket", "account_number"],
        right_on=["trade_ticket", "account_number"],
        how="left"
    )

df = ResearchInsights.add_confidence_bucket(df)

if df.empty:
    command_card(
        "No trades",
        "Import trades before using Research Lab.",
        "Go to Import."
    )
    st.stop()

section("Research Filters")

symbols = ["All"] + sorted(df["symbol"].dropna().unique().tolist()) if "symbol" in df.columns else ["All"]
sessions = ["All"] + sorted(df["session"].dropna().unique().tolist()) if "session" in df.columns else ["All"]

col1, col2, col3 = st.columns(3)

with col1:
    symbol = st.selectbox("Symbol", symbols)

with col2:
    session = st.selectbox("Session", sessions)

with col3:
    result = st.selectbox("Result", ["All", "Win", "Loss", "Breakeven"])

direction = st.selectbox("Direction", ["All", "BUY", "SELL"])

compare = st.selectbox(
    "Compare By",
    [
        None,
        "symbol",
        "session",
        "direction",
        "trade_grade",
        "mistake_type",
        "confidence_bucket",
    ]
)

filtered, stats, comparison = ResearchQueries.run(
    df,
    symbol=symbol,
    session=session,
    direction=direction,
    result=result,
    compare_by=compare,
)

section("Research Summary")

stat_row([
    {"label": "Trades", "value": stats["total_trades"], "helper": "Filtered trades", "status": "neutral"},
    {"label": "Win %", "value": f'{stats["win_rate"]}%', "helper": "Win rate", "status": "positive"},
])

stat_row([
    {"label": "Net Profit", "value": stats["net_profit"], "helper": "Filtered net result", "status": "positive" if stats["net_profit"] >= 0 else "negative"},
    {"label": "Profit Factor", "value": stats["profit_factor"], "helper": "Gross profit / gross loss", "status": "positive"},
])

stat_row([
    {"label": "Average Win", "value": stats["average_win"], "helper": "Winning trades", "status": "positive"},
    {"label": "Average Loss", "value": stats["average_loss"], "helper": "Losing trades", "status": "negative"},
])

stat_row([
    {"label": "Expectancy", "value": stats["expectancy"], "helper": "Expected result per trade", "status": "neutral"},
])

section("Quick Insights")

best_symbol, worst_symbol = ResearchInsights.best_and_worst(filtered, "symbol")
best_session, worst_session = ResearchInsights.best_and_worst(filtered, "session")
most_expensive_mistake = ResearchInsights.most_expensive_mistake(filtered)

stat_row([
    {"label": "Best Symbol", "value": best_symbol, "helper": "Highest net profit", "status": "positive"},
    {"label": "Worst Symbol", "value": worst_symbol, "helper": "Lowest net profit", "status": "negative"},
])

stat_row([
    {"label": "Best Session", "value": best_session, "helper": "Highest net profit", "status": "positive"},
    {"label": "Worst Session", "value": worst_session, "helper": "Lowest net profit", "status": "negative"},
])

stat_row([
    {"label": "Costliest Mistake", "value": most_expensive_mistake, "helper": "Lowest net result", "status": "negative"},
])

if not comparison.empty:
    section("Comparison")
    st.dataframe(comparison, use_container_width=True, hide_index=True)

section("Filtered Trades")
st.dataframe(filtered, use_container_width=True, hide_index=True)
