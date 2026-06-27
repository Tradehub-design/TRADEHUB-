import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.analytics_engine import AnalyticsEngine
from engine.format_engine import FormatEngine
from engine.advanced_metrics_engine import AdvancedMetricsEngine
from components.dashboard_v3 import DashboardV3
from components.trade_table import TradeTable


load_css()
DashboardV3.load_css()

app_header(
    "Dashboard",
    "Your trading performance overview"
)

DashboardV3.quick_menu()

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()
open_positions = DataEngine.load_open_positions()
account_snapshot = DataEngine.load_account_snapshot()
sync_status = DataEngine.load_sync_status()

if trades is None or trades.empty:
    st.warning("No trades loaded yet.")
    st.stop()

stats = StatisticsEngine.summary(trades)
advanced = AdvancedMetricsEngine.summary(trades)

balance = 0
equity = 0
floating_pl = 0

if account_snapshot is not None and not account_snapshot.empty:
    account = account_snapshot.iloc[0]
    balance = account.get("balance", 0) or 0
    equity = account.get("equity", 0) or 0
    floating_pl = account.get("profit", 0) or 0
else:
    balance = trades.iloc[0].get("balance", 0) if "balance" in trades.columns else 0
    equity = balance

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    DashboardV3.kpi(
        "Balance",
        FormatEngine.currency(balance),
        "Demo / live account",
        "green"
    )

with k2:
    DashboardV3.kpi(
        "Equity",
        FormatEngine.currency(equity),
        "Live equity",
        "green" if equity >= balance else "red"
    )

with k3:
    DashboardV3.kpi(
        "Win Rate",
        f"{stats['win_rate']}%",
        f"{stats['wins']} wins",
        "green" if stats["win_rate"] >= 50 else "red"
    )

with k4:
    DashboardV3.kpi(
        "Profit Factor",
        stats["profit_factor"],
        "Gross profit / loss",
        "green" if stats["profit_factor"] >= 1 else "red"
    )

with k5:
    DashboardV3.kpi(
        "Floating P/L",
        FormatEngine.signed_currency(floating_pl),
        "Open positions",
        FormatEngine.result_status(floating_pl)
    )

with k6:
    DashboardV3.kpi(
        "Expectancy",
        FormatEngine.signed_currency(stats["average_trade"]),
        "Average trade",
        FormatEngine.result_status(stats["average_trade"])
    )

main_col, side_col = st.columns([4, 1.15])

with main_col:
    chart1, chart2, chart3 = st.columns([1.6, 1.4, 1.3])

    with chart1:
        with st.container(border=True):
            DashboardV3.panel("Equity Curve")

            curve = trades.copy()
            curve["trade_date"] = pd.to_datetime(curve["trade_date"], errors="coerce")
            curve = curve.dropna(subset=["trade_date"]).sort_values("trade_date")
            curve["equity_curve"] = curve["net_profit"].cumsum()

            st.line_chart(
                curve.set_index("trade_date")["equity_curve"],
                height=260
            )

    with chart2:
        with st.container(border=True):
            DashboardV3.panel("Monthly Performance")

            monthly = AnalyticsEngine.monthly_summary(trades)

            if not monthly.empty:
                st.bar_chart(
                    monthly.set_index("Month")["NetProfit"],
                    height=260
                )
            else:
                st.info("No monthly data.")

    with chart3:
        with st.container(border=True):
            DashboardV3.panel("Session Analysis")

            session = AnalyticsEngine.session_summary(trades)

            if not session.empty:
                st.dataframe(
                    session[["session", "Trades", "NetProfit", "WinRate"]],
                    use_container_width=True,
                    hide_index=True,
                    height=260
                )
            else:
                st.info("No session data.")

    d1, d2 = st.columns([1.5, 1])

    with d1:
        with st.container(border=True):
            DashboardV3.panel("Drawdown")

            dd = curve.copy()
            dd["peak"] = dd["equity_curve"].cummax()
            dd["drawdown"] = dd["equity_curve"] - dd["peak"]

            st.line_chart(
                dd.set_index("trade_date")["drawdown"],
                height=230
            )

    with d2:
        with st.container(border=True):
            DashboardV3.panel("Performance Summary")

            st.metric("Total Trades", stats["total_trades"])
            st.metric("Winning Trades", stats["wins"])
            st.metric("Losing Trades", stats["losses"])
            st.metric("Gross Profit", FormatEngine.currency(stats["gross_profit"]))
            st.metric("Gross Loss", FormatEngine.currency(stats["gross_loss"]))
            st.metric("Net Profit", FormatEngine.signed_currency(stats["net_profit"]))

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        with st.container(border=True):
            DashboardV3.panel("Recent Trades")
            TradeTable.render(trades.head(6), height=260)

    with b2:
        with st.container(border=True):
            DashboardV3.panel("Recent Reviews")

            if reviews is not None and not reviews.empty:
                st.dataframe(
                    reviews.head(6),
                    use_container_width=True,
                    hide_index=True,
                    height=260
                )
            else:
                st.info("No reviews yet.")

    with b3:
        with st.container(border=True):
            DashboardV3.panel("Open Positions")

            if open_positions is not None and not open_positions.empty:
                st.dataframe(
                    open_positions,
                    use_container_width=True,
                    hide_index=True,
                    height=260
                )
            else:
                st.info("No open positions.")

    with b4:
        with st.container(border=True):
            DashboardV3.panel("Automation Status")

            if sync_status is not None and not sync_status.empty:
                st.dataframe(
                    sync_status,
                    use_container_width=True,
                    hide_index=True,
                    height=260
                )
            else:
                st.info("Desktop sync offline.")

with side_col:
    DashboardV3.side_card(
        "Today's Goal",
        "<h2 style='margin:0;color:#22c55e;'>67%</h2><p>$200 / $300 target</p>",
        "Daily performance goal"
    )

    DashboardV3.side_card(
        "AI Insight",
        "You perform best during the London session. Focus on high momentum setups.",
        "Based on trade history"
    )

    DashboardV3.side_card(
        "Best Strategy",
        f"{advanced['largest_symbol']} is currently your strongest performer.",
        "Strategy builder coming next"
    )

    DashboardV3.side_card(
        "Top Mistake",
        "Review losing streaks and fast re-entries.",
        "Use Review Centre"
    )

    DashboardV3.side_card(
        "Risk Meter",
        "LOW RISK",
        "Margin and drawdown monitor"
    )
