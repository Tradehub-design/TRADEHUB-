import streamlit as st

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card, table_header, mini_card, trade_quality_card
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.health_engine import HealthEngine
from engine.analytics_engine import AnalyticsEngine
from engine.edge_score import EdgeScoreEngine


load_css()

app_header(
    "🏠 Command Centre",
    "Your trading cockpit — performance, live sync, edge, risk and recent activity."
)

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()
account_snapshot = DataEngine.load_account_snapshot()
open_positions = DataEngine.load_open_positions()
sync_status = DataEngine.load_sync_status()

section("Live Status")

if sync_status.empty:
    stat_row([
        {
            "label": "MT5 Sync",
            "value": "Offline",
            "helper": "Desktop agent not connected",
            "status": "warning",
        },
        {
            "label": "Open Positions",
            "value": len(open_positions),
            "helper": "Live positions",
            "status": "neutral",
        },
    ])
else:
    status = sync_status.iloc[0]

    stat_row([
        {
            "label": "MT5 Sync",
            "value": status.get("status", "unknown"),
            "helper": status.get("message", ""),
            "status": "positive" if status.get("status") == "connected" else "warning",
        },
        {
            "label": "Last Sync",
            "value": status.get("last_sync", "-"),
            "helper": "Desktop agent",
            "status": "neutral",
        },
    ])

if not account_snapshot.empty:
    account = account_snapshot.iloc[0]

    stat_row([
        {
            "label": "Balance",
            "value": account.get("balance", 0),
            "helper": "Live account",
            "status": "neutral",
        },
        {
            "label": "Equity",
            "value": account.get("equity", 0),
            "helper": "Live equity",
            "status": "positive" if account.get("equity", 0) >= account.get("balance", 0) else "negative",
        },
        {
            "label": "Floating P/L",
            "value": account.get("profit", 0),
            "helper": "Open positions",
            "status": "positive" if account.get("profit", 0) >= 0 else "negative",
        },
    ])

if trades is None or trades.empty:
    command_card(
        "No trades found",
        "Import trades or run MT5 Sync to activate your dashboard.",
        "Go to Import or run sync agent."
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
        "label": "Trading Health",
        "value": health_score,
        "helper": f"Grade {health_grade}",
        "status": "positive" if health_score >= 75 else "warning",
    },
])

section("Performance Overview")

monthly = AnalyticsEngine.monthly_summary(trades)

left, right = st.columns([1.4, 1])

with left:
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
            command_card("Edge Score", "No reviewed trades yet.", "Complete Trade Review.")
    else:
        command_card("Edge Score", "No reviewed trades yet.", "Complete Trade Review.")

section("Quick Intelligence")

symbol_summary = AnalyticsEngine.symbol_summary(trades)
session_summary = AnalyticsEngine.session_summary(trades)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if not symbol_summary.empty:
        row = symbol_summary.iloc[0]
        mini_card("Best Symbol", row["symbol"], f"Net {round(row['NetProfit'], 2)}", "positive", "🏆")

with col2:
    if not symbol_summary.empty:
        row = symbol_summary.iloc[-1]
        mini_card("Worst Symbol", row["symbol"], f"Net {round(row['NetProfit'], 2)}", "negative", "⚠️")

with col3:
    if not session_summary.empty:
        row = session_summary.iloc[0]
        mini_card("Best Session", row["session"], f"Net {round(row['NetProfit'], 2)}", "positive", "☀️")

with col4:
    if not session_summary.empty:
        row = session_summary.iloc[-1]
        mini_card("Worst Session", row["session"], f"Net {round(row['NetProfit'], 2)}", "negative", "🌙")

section("Open Positions")

if open_positions.empty:
    command_card(
        "No open positions",
        "Open positions will appear here once MT5 Sync is running.",
        "Live monitoring."
    )
else:
    table_header(
        "Open Positions",
        f"{len(open_positions)} active positions"
    )

    st.dataframe(
        open_positions,
        use_container_width=True,
        hide_index=True
    )

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
    "Your latest trading activity."
)

st.dataframe(
    trades[recent_cols].head(12),
    use_container_width=True,
    hide_index=True
)
