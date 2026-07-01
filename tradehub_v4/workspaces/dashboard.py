import streamlit as st
from engine.statistics_engine import StatisticsEngine
from engine.analytics_engine import AnalyticsEngine
from engine.format_engine import FormatEngine
from tradehub_v4.core.state import AppState
from tradehub_v4.core.ui import UI
from tradehub_v4.services.trade_math import equity_curve


class DashboardWorkspace:
    @staticmethod
    def render():
        UI.header("Dashboard", "Trading command centre for performance, risk, automation and insights.")

        trades = AppState.trades()
        reviews = AppState.reviews()
        account = AppState.account_snapshot()
        open_positions = AppState.open_positions()
        sync_status = AppState.sync_status()

        if trades is None or trades.empty:
            st.warning("No trade data found. Import trades or keep the seed data enabled.")
            return

        stats = StatisticsEngine.summary(trades)
        curve = equity_curve(trades)

        balance = 0
        equity = 0
        floating = 0
        if account is not None and not account.empty:
            row = account.iloc[0]
            balance = row.get("balance", 0) or 0
            equity = row.get("equity", 0) or 0
            floating = row.get("profit", 0) or 0
        elif "balance" in trades.columns:
            balance = trades.iloc[0].get("balance", 0) or 0
            equity = balance

        k1, k2, k3, k4, k5, k6 = st.columns(6)
        with k1:
            UI.kpi("Balance", FormatEngine.currency(balance), "Account balance")
        with k2:
            UI.kpi("Equity", FormatEngine.currency(equity), "Live/demo equity")
        with k3:
            UI.kpi("Win Rate", f"{stats['win_rate']}%", f"{stats['wins']} wins", "positive" if stats["win_rate"] >= 50 else "negative")
        with k4:
            UI.kpi("Profit Factor", stats["profit_factor"], "Gross profit / loss", "positive" if stats["profit_factor"] >= 1 else "negative")
        with k5:
            UI.kpi("Floating P/L", FormatEngine.signed_currency(floating), "Open trades", FormatEngine.result_status(floating))
        with k6:
            UI.kpi("Expectancy", FormatEngine.signed_currency(stats["average_trade"]), "Average trade", FormatEngine.result_status(stats["average_trade"]))

        main, side = st.columns([4, 1.15])
        with main:
            c1, c2, c3 = st.columns([1.6, 1.3, 1.2])
            with c1:
                UI.section("Equity Curve")
                if not curve.empty:
                    st.line_chart(curve.set_index("trade_date")["equity_curve"], height=280)
                else:
                    st.info("No equity curve data.")
            with c2:
                UI.section("Monthly Performance")
                monthly = AnalyticsEngine.monthly_summary(trades)
                if not monthly.empty:
                    st.bar_chart(monthly.set_index("Month")["NetProfit"], height=280)
                else:
                    st.info("No monthly data.")
            with c3:
                UI.section("Session Analysis")
                session = AnalyticsEngine.session_summary(trades)
                if not session.empty:
                    st.dataframe(session, use_container_width=True, hide_index=True, height=280)
                else:
                    st.info("No session data.")

            d1, d2 = st.columns([1.6, 1])
            with d1:
                UI.section("Drawdown")
                if not curve.empty:
                    st.line_chart(curve.set_index("trade_date")["drawdown"], height=260)
                else:
                    st.info("No drawdown data.")
            with d2:
                UI.section("Performance Summary")
                st.metric("Total Trades", stats["total_trades"])
                st.metric("Winning Trades", stats["wins"])
                st.metric("Losing Trades", stats["losses"])
                st.metric("Net Profit", FormatEngine.signed_currency(stats["net_profit"]))

            b1, b2, b3 = st.columns(3)
            with b1:
                UI.section("Recent Trades")
                st.dataframe(trades.head(8), use_container_width=True, hide_index=True, height=300)
            with b2:
                UI.section("Open Positions")
                if open_positions is not None and not open_positions.empty:
                    st.dataframe(open_positions, use_container_width=True, hide_index=True, height=300)
                else:
                    st.info("No open positions.")
            with b3:
                UI.section("Automation")
                if sync_status is not None and not sync_status.empty:
                    st.dataframe(sync_status, use_container_width=True, hide_index=True, height=300)
                else:
                    st.info("Sync offline.")

        with side:
            UI.card("Today's Goal", "<h2 class='green'>67%</h2><p>$200 / $300 target</p>", "Daily target")
            UI.card("AI Insight", "Your best results come from focusing on high-quality sessions and avoiding fast re-entries.", "Rule-based insight")
            best_symbol = "-"
            symbols = AnalyticsEngine.symbol_summary(trades)
            if not symbols.empty:
                best_symbol = symbols.iloc[0]["symbol"]
            UI.card("Best Market", f"<h3>{best_symbol}</h3>", "Highest total P/L")
            UI.card("Risk Meter", "<h3 class='green'>LOW RISK</h3>", "Margin and drawdown monitor")
