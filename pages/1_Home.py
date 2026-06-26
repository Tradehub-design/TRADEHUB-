import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.health_engine import HealthEngine
from engine.analytics_engine import AnalyticsEngine
from engine.edge_score import EdgeScoreEngine
from engine.grade import GradeEngine


load_css()

app_header(
    "🏠 Command Centre",
    "Your trading cockpit — performance, edge, reviews, risk and recent activity."
)

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades to activate your dashboard.",
        "Go to Import when ready."
    )
    st.stop()

stats = StatisticsEngine.summary(trades)
health_score = HealthEngine.score(trades)
health_grade = HealthEngine.grade(health_score)

section("Performance Snapshot")

stat_row([
    {
        "label": "Net Profit",
        "value": stats["net_profit"],
        "helper": "Total closed result",
        "status": "positive" if stats["net_profit"] >= 0 else "negative",
    },
    {
        "label": "Win Rate",
        "value": f"{stats['win_rate']}%",
        "helper": f"{stats['wins']} wins / {stats['total_trades']} trades",
        "status": "positive" if stats["win_rate"] >= 50 else "negative",
    },
    {
        "label": "Profit Factor",
        "value": stats["profit_factor"],
        "helper": "Gross profit / gross loss",
        "status": "positive" if stats["profit_factor"] >= 1 else "negative",
    },
])

stat_row([
    {
        "label": "Average Trade",
        "value": stats["average_trade"],
        "helper": "Average result",
        "status": "positive" if stats["average_trade"] >= 0 else "negative",
    },
    {
        "label": "Trading Health",
        "value": health_score,
        "helper": f"Grade {health_grade}",
        "status": "positive" if health_score >= 75 else "warning",
    },
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "Imported trades",
        "status": "neutral",
    },
])

section("Edge Score")

if reviews is not None and not reviews.empty:
    merged = trades.merge(
        reviews,
        left_on=["ticket", "account_number"],
        right_on=["trade_ticket", "account_number"],
        how="inner"
    )

    edge_scores = []

    for _, row in merged.iterrows():
        row_data = row.to_dict()
        edge_scores.append(
            EdgeScoreEngine.calculate(row_data, row_data)
        )

    if edge_scores:
        avg_edge = round(sum(edge_scores) / len(edge_scores), 1)
        best_edge = max(edge_scores)
        worst_edge = min(edge_scores)

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
    else:
        command_card(
            "No reviewed trades yet",
            "Complete trade reviews to activate Edge Score.",
            "Trade Review will power your execution quality."
        )
else:
    command_card(
        "No journal reviews yet",
        "Review trades to unlock Edge Score and AI-style insights.",
        "Start with your most recent trade."
    )

section("Performance Overview")

monthly = AnalyticsEngine.monthly_summary(trades)

if not monthly.empty:
    st.line_chart(
        monthly.set_index("Month")["NetProfit"]
    )
else:
    st.info("Monthly performance will appear once trade dates are available.")

section("Best / Worst")

symbol_summary = AnalyticsEngine.symbol_summary(trades)
session_summary = AnalyticsEngine.session_summary(trades)

if not symbol_summary.empty:
    best_symbol = symbol_summary.iloc[0]
    worst_symbol = symbol_summary.iloc[-1]

    stat_row([
        {
            "label": "Best Symbol",
            "value": best_symbol["symbol"],
            "helper": f"Net {round(best_symbol['NetProfit'], 2)}",
            "status": "positive",
        },
        {
            "label": "Worst Symbol",
            "value": worst_symbol["symbol"],
            "helper": f"Net {round(worst_symbol['NetProfit'], 2)}",
            "status": "negative",
        },
    ])

if not session_summary.empty:
    best_session = session_summary.iloc[0]
    worst_session = session_summary.iloc[-1]

    stat_row([
        {
            "label": "Best Session",
            "value": best_session["session"],
            "helper": f"Net {round(best_session['NetProfit'], 2)}",
            "status": "positive",
        },
        {
            "label": "Worst Session",
            "value": worst_session["session"],
            "helper": f"Net {round(worst_session['NetProfit'], 2)}",
            "status": "negative",
        },
    ])

section("Recent Trades")

recent_cols = [
    col for col in [
        "ticket",
        "trade_date",
        "symbol",
        "direction",
        "net_profit",
        "session",
    ]
    if col in trades.columns
]

table_header(
    "Recent Trades",
    "Your latest imported trading activity."
)

st.dataframe(
    trades[recent_cols].head(12),
    use_container_width=True,
    hide_index=True
)
