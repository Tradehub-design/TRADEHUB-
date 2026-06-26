import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header
from data.data_engine import DataEngine
from research.queries import ResearchQueries
from research.insights import ResearchInsights
from engine.edge_score import EdgeScoreEngine
from engine.grade import GradeEngine


load_css()

app_header(
    "🔬 Research Lab",
    "Filter, compare and study your trades to find what is actually working."
)

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades before using Research Lab.",
        "Go to Import."
    )
    st.stop()

df = trades.copy()

if reviews is not None and not reviews.empty:
    df = df.merge(
        reviews,
        left_on=["ticket", "account_number"],
        right_on=["trade_ticket", "account_number"],
        how="left"
    )

    edge_scores = []
    edge_grades = []

    for _, row in df.iterrows():
        row_data = row.to_dict()

        if pd.notna(row_data.get("trade_ticket")):
            edge = EdgeScoreEngine.calculate(row_data, row_data)
            grade = GradeEngine.grade(edge)
        else:
            edge = None
            grade = None

        edge_scores.append(edge)
        edge_grades.append(grade)

    df["edge_score"] = edge_scores
    df["edge_grade"] = edge_grades

df = ResearchInsights.add_confidence_bucket(df)

section("Filters")

symbols = ["All"] + sorted(df["symbol"].dropna().unique().tolist()) if "symbol" in df.columns else ["All"]
sessions = ["All"] + sorted(df["session"].dropna().unique().tolist()) if "session" in df.columns else ["All"]

col1, col2, col3 = st.columns(3)

with col1:
    symbol = st.selectbox("Symbol", symbols)

with col2:
    session = st.selectbox("Session", sessions)

with col3:
    result = st.selectbox(
        "Result",
        ["All", "Win", "Loss", "Breakeven"]
    )

direction = st.selectbox(
    "Direction",
    ["All", "BUY", "SELL"]
)

compare_options = [
    None,
    "symbol",
    "session",
    "direction",
]

for optional_col in [
    "trade_grade",
    "mistake_type",
    "confidence_bucket",
    "edge_grade",
]:
    if optional_col in df.columns:
        compare_options.append(optional_col)

compare = st.selectbox(
    "Compare By",
    compare_options
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
    {
        "label": "Trades",
        "value": stats["total_trades"],
        "helper": "Filtered trades",
        "status": "neutral",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": "Filtered win rate",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
    {
        "label": "Net Profit",
        "value": stats["net_profit"],
        "helper": "Filtered result",
        "status": "positive" if stats["net_profit"] >= 0 else "negative",
    },
])

stat_row([
    {
        "label": "Profit Factor",
        "value": stats["profit_factor"],
        "helper": "Gross profit / loss",
        "status": "positive" if stats["profit_factor"] >= 1 else "negative",
    },
    {
        "label": "Average Win",
        "value": stats["average_win"],
        "helper": "Winning trades",
        "status": "positive",
    },
    {
        "label": "Average Loss",
        "value": stats["average_loss"],
        "helper": "Losing trades",
        "status": "negative",
    },
])

if "edge_score" in filtered.columns and filtered["edge_score"].notna().any():
    section("Edge Quality")

    avg_edge = round(filtered["edge_score"].dropna().mean(), 1)
    best_edge = int(filtered["edge_score"].dropna().max())
    worst_edge = int(filtered["edge_score"].dropna().min())

    stat_row([
        {
            "label": "Average Edge",
            "value": avg_edge,
            "helper": "Execution quality",
            "status": "positive" if avg_edge >= 80 else "warning",
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

section("Quick Insights")

best_symbol, worst_symbol = ResearchInsights.best_and_worst(filtered, "symbol")
best_session, worst_session = ResearchInsights.best_and_worst(filtered, "session")
costliest_mistake = ResearchInsights.most_expensive_mistake(filtered)

stat_row([
    {
        "label": "Best Symbol",
        "value": best_symbol,
        "helper": "Highest net profit",
        "status": "positive",
    },
    {
        "label": "Worst Symbol",
        "value": worst_symbol,
        "helper": "Lowest net profit",
        "status": "negative",
    },
    {
        "label": "Costliest Mistake",
        "value": costliest_mistake,
        "helper": "Worst mistake impact",
        "status": "negative",
    },
])

if not comparison.empty:
    section("Comparison")

    table_header(
        "Comparison Table",
        f"Grouped by {compare}"
    )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

section("Filtered Trades")

display_cols = [
    col for col in [
        "ticket",
        "trade_date",
        "symbol",
        "direction",
        "net_profit",
        "session",
        "trade_grade",
        "mistake_type",
        "confidence_score",
        "edge_score",
        "edge_grade",
    ]
    if col in filtered.columns
]

table_header(
    "Trades",
    "Filtered results based on your research criteria."
)

st.dataframe(
    filtered[display_cols],
    use_container_width=True,
    hide_index=True
)
