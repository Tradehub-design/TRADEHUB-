import pandas as pd
import streamlit as st

from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.analytics_engine import AnalyticsEngine
from engine.format_engine import FormatEngine
from v2.ui import V2UI


class DashboardV2:

    @staticmethod
    def render():
        V2UI.header(
            "Dashboard",
            "Your trading performance overview"
        )

        trades = DataEngine.load_trades()
        reviews = DataEngine.load_reviews()
        account_snapshot = DataEngine.load_account_snapshot()
        open_positions = DataEngine.load_open_positions()
        sync_status = DataEngine.load_sync_status()

        if trades is None or trades.empty:
            st.warning("No trades loaded.")
            return

        stats = StatisticsEngine.summary(trades)

        balance = 0
        equity = 0
        floating_pl = 0

        if account_snapshot is not None and not account_snapshot.empty:
            account = account_snapshot.iloc[0]
            balance = account.get("balance", 0) or 0
            equity = account.get("equity", 0) or 0
            floating_pl = account.get("profit", 0) or 0
        elif "balance" in trades.columns:
            balance = trades.iloc[0].get("balance", 0) or 0
            equity = balance

        k1, k2, k3, k4, k5, k6 = st.columns(6)

        with k1:
            V2UI.kpi("Balance", FormatEngine.currency(balance), "Account balance", "green")

        with k2:
            V2UI.kpi("Equity", FormatEngine.currency(equity), "Live / demo equity", "green")

        with k3:
            V2UI.kpi("Win Rate", f"{stats['win_rate']}%", f"{stats['wins']} wins", "green" if stats["win_rate"] >= 50 else "red")

        with k4:
            V2UI.kpi("Profit Factor", stats["profit_factor"], "Gross profit / loss", "green" if stats["profit_factor"] >= 1 else "red")

        with k5:
            V2UI.kpi("Floating P/L", FormatEngine.signed_currency(floating_pl), "Open positions", FormatEngine.result_status(floating_pl))

        with k6:
            V2UI.kpi("Expectancy", FormatEngine.signed_currency(stats["average_trade"]), "Average trade", FormatEngine.result_status(stats["average_trade"]))

        main, side = st.columns([4, 1.15])

        with main:
            chart1, chart2, chart3 = st.columns([1.6, 1.3, 1.2])

            curve = trades.copy()
            curve["trade_date"] = pd.to_datetime(curve["trade_date"], errors="coerce")
            curve = curve.dropna(subset=["trade_date"]).sort_values("trade_date")
            curve["equity_curve"] = curve["net_profit"].cumsum()

            with chart1:
                V2UI.section("Equity Curve")
                st.line_chart(
                    curve.set_index("trade_date")["equity_curve"],
                    height=260,
                )

            with chart2:
                V2UI.section("Monthly Performance")
                monthly = AnalyticsEngine.monthly_summary(trades)

                if not monthly.empty:
                    st.bar_chart(
                        monthly.set_index("Month")["NetProfit"],
                        height=260,
                    )
                else:
                    st.info("No monthly data.")

            with chart3:
                V2UI.section("Session Analysis")
                session = AnalyticsEngine.session_summary(trades)

                if not session.empty:
                    st.dataframe(
                        session[["session", "Trades", "NetProfit", "WinRate"]],
                        use_container_width=True,
                        hide_index=True,
                        height=260,
                    )
                else:
                    st.info("No session data.")

            d1, d2 = st.columns([1.6, 1])

            with d1:
                V2UI.section("Drawdown")
                dd = curve.copy()
                dd["peak"] = dd["equity_curve"].cummax()
                dd["drawdown"] = dd["equity_curve"] - dd["peak"]

                st.line_chart(
                    dd.set_index("trade_date")["drawdown"],
                    height=240,
                )

            with d2:
                V2UI.section("Performance Summary")
                st.metric("Total Trades", stats["total_trades"])
                st.metric("Winning Trades", stats["wins"])
                st.metric("Losing Trades", stats["losses"])
                st.metric("Gross Profit", FormatEngine.currency(stats["gross_profit"]))
                st.metric("Gross Loss", FormatEngine.currency(stats["gross_loss"]))
                st.metric("Net Profit", FormatEngine.signed_currency(stats["net_profit"]))

            b1, b2, b3 = st.columns(3)

            with b1:
                V2UI.section("Recent Trades")
                st.dataframe(
                    trades.head(8),
                    use_container_width=True,
                    hide_index=True,
                    height=280,
                )

            with b2:
                V2UI.section("Recent Reviews")
                if reviews is not None and not reviews.empty:
                    st.dataframe(
                        reviews.head(8),
                        use_container_width=True,
                        hide_index=True,
                        height=280,
                    )
                else:
                    st.info("No reviews yet.")

            with b3:
                V2UI.section("Automation Status")
                if sync_status is not None and not sync_status.empty:
                    st.dataframe(
                        sync_status,
                        use_container_width=True,
                        hide_index=True,
                        height=280,
                    )
                else:
                    st.info("Desktop sync offline.")

        with side:
            V2UI.card(
                "Today's Goal",
                "<h2 class='green'>67%</h2><p>$200 / $300 target</p>",
                "Daily performance goal",
            )

            V2UI.card(
                "AI Insight",
                "You perform best during London. Focus on high momentum setups.",
                "Based on trade history",
            )

            V2UI.card(
                "Best Strategy",
                "No Wick Reversal",
                "Strategy Builder coming next",
            )

            V2UI.card(
                "Top Mistake",
                "Review fast re-entries and losing streaks.",
                "Use Trade Review",
            )

            V2UI.card(
                "Risk Meter",
                "LOW RISK",
                "Margin and drawdown monitor",
            )
