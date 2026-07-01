import streamlit as st
from engine.analytics_engine import AnalyticsEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from tradehub_v4.core.state import AppState
from tradehub_v4.core.ui import UI
from tradehub_v4.services.trade_math import prepare_trades, group_summary, equity_curve


class AnalyticsWorkspace:
    @staticmethod
    def render():
        UI.header("Analytics", "Symbols, sessions, weekdays, months, hours, drawdown and risk.")
        df = prepare_trades(AppState.trades())
        if df.empty:
            st.warning("No trades found.")
            return

        tabs = st.tabs(["Overview", "Symbols", "Sessions", "Weekdays", "Months", "Hours", "Drawdown", "Risk", "Accounts"])
        with tabs[0]:
            stats = StatisticsEngine.summary(df)
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Trades", stats["total_trades"])
            c2.metric("Net P/L", FormatEngine.signed_currency(stats["net_profit"]))
            c3.metric("Win Rate", f"{stats['win_rate']}%")
            c4.metric("Profit Factor", stats["profit_factor"])
            c5.metric("Average", FormatEngine.signed_currency(stats["average_trade"]))
            curve = equity_curve(df)
            if not curve.empty:
                st.line_chart(curve.set_index("trade_date")["equity_curve"], height=320)
        with tabs[1]:
            result = AnalyticsEngine.symbol_summary(df); st.dataframe(result, use_container_width=True, hide_index=True)
            if not result.empty: st.bar_chart(result.set_index("symbol")["NetProfit"])
        with tabs[2]:
            result = AnalyticsEngine.session_summary(df); st.dataframe(result, use_container_width=True, hide_index=True)
            if not result.empty: st.bar_chart(result.set_index("session")["NetProfit"])
        with tabs[3]:
            result = group_summary(df, "weekday"); st.dataframe(result, use_container_width=True, hide_index=True)
            if not result.empty: st.bar_chart(result.set_index("weekday")["NetProfit"])
        with tabs[4]:
            result = group_summary(df, "month"); st.dataframe(result, use_container_width=True, hide_index=True)
            if not result.empty: st.bar_chart(result.set_index("month")["NetProfit"])
        with tabs[5]:
            result = group_summary(df, "hour"); st.dataframe(result, use_container_width=True, hide_index=True)
            if not result.empty: st.bar_chart(result.set_index("hour")["NetProfit"])
        with tabs[6]:
            curve = equity_curve(df)
            if curve.empty:
                st.info("No drawdown data.")
            else:
                st.line_chart(curve.set_index("trade_date")["drawdown"], height=320)
                st.metric("Max Drawdown", FormatEngine.signed_currency(curve["drawdown"].min()))
                st.dataframe(curve[["ticket", "trade_date", "symbol", "direction", "net_profit", "equity_curve", "drawdown"]], use_container_width=True, hide_index=True)
        with tabs[7]:
            stats = StatisticsEngine.summary(df)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Average Win", FormatEngine.signed_currency(stats["average_win"]))
            c2.metric("Average Loss", FormatEngine.signed_currency(stats["average_loss"]))
            c3.metric("Gross Profit", FormatEngine.currency(stats["gross_profit"]))
            c4.metric("Gross Loss", FormatEngine.currency(stats["gross_loss"]))
            if "hold_minutes" in df.columns:
                hold = df["hold_minutes"].dropna()
                if not hold.empty:
                    st.metric("Average Hold Minutes", round(hold.mean(), 1))
                    st.bar_chart(hold)
        with tabs[8]:
            if "account_number" in df.columns:
                st.dataframe(group_summary(df, "account_number"), use_container_width=True, hide_index=True)
            else:
                st.info("No account number data available.")
