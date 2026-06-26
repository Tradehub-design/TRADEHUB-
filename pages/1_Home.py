import streamlit as st

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header, mini_card, trade_quality_card
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
    {
        "label": "Average Trade",
        "value": stats["average_trade"],
        "helper": "Average result",
        "status": "positive" if stats["average_trade"] >= 0 else "negative",
    },
])

stat_row([
    {
        "label": "Total Trades",
        "value": stats["total_trades"],
        "helper": "Imported trades",
        "status": "neutral",
    },
    {
        "label": "Trading Health",
        "value": health_score,
        "helper": f"Grade {health_grade}",
        "status": "positive" if health_score >= 75 else "warning",
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

section("Performance Overview")

monthly = AnalyticsEngine.monthly_summary(trades)

left, right = st.columns([1.4, 1])

with left:
    command_card(
        "Performance Curve",
        "Your closed trade equity curve based on imported trade history.",
        "Live balance will connect after MT5 Sync."
    )

    if not monthly.empty:
        st.line_chart(
            monthly.set_index("Month")["NetProfit"]
        )
    else:
        st.info("Monthly performance will appear once trade dates are available.")

with right:
    if reviews is not None and not reviews.empty:
        merged = trades.merge(
            reviews,
            left_on=["ticket", "account_number"],
            right_on=["trade_ticket", "account_number"],
            how="inner"
        )

        edge_scores = []

        for _, row in merged.iterrows():
            data = row.to_dict()
            edge_scores.append(EdgeScoreEngine.calculate(data, data))

        if edge_scores:
            avg_edge = round(sum(edge_scores) / len(edge_scores), 1)
            trade_quality_card(
                int(avg_edge),
                f"{len(edge_scores)} reviewed trades"
            )
        else:
            command_card(
                "Edge Score Overview",
                "No reviewed trades yet.",
                "Complete Trade Review to unlock this."
            )
    else:
        command_card(
            "Edge Score Overview",
            "No reviewed trades yet.",
            "Complete Trade Review to unlock this."
        )

section("Quick Intelligence")

symbol_summary = AnalyticsEngine.symbol_summary(trades)
session_summary = AnalyticsEngine.session_summary(trades)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if not symbol_summary.empty:
        row = symbol_summary.iloc[0]
        mini_card("Best Symbol", row["symbol"], f"Net {round(row['NetProfit'], 2)}", "positive", "🏆")
    else:
        mini_card("Best Symbol", "N/A", "Insufficient data", "neutral", "🏆")

with col2:
    if not symbol_summary.empty:
        row = symbol_summary.iloc[-1]
        mini_card("Worst Symbol", row["symbol"], f"Net {round(row['NetProfit'], 2)}", "negative", "⚠️")
    else:
        mini_card("Worst Symbol", "N/A", "Insufficient data", "neutral", "⚠️")

with col3:
    if not session_summary.empty:
        row = session_summary.iloc[0]
        mini_card("Best Session", row["session"], f"Net {round(row['NetProfit'], 2)}", "positive", "☀️")
    else:
        mini_card("Best Session", "N/A", "Insufficient data", "neutral", "☀️")

with col4:
    if not session_summary.empty:
        row = session_summary.iloc[-1]
        mini_card("Worst Session", row["session"], f"Net {round(row['NetProfit'], 2)}", "negative", "🌙")
    else:
        mini_card("Worst Session", "N/A", "Insufficient data", "neutral", "🌙")

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
