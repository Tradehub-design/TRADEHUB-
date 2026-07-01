import pandas as pd
import streamlit as st
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from tradehub_v4.core.state import AppState
from tradehub_v4.core.ui import UI
from tradehub_v4.services.trade_math import prepare_trades, daily_summary
from tradehub_v4.core.calendar_ui import CalendarUI


class TradeReviewsWorkspace:
    @staticmethod
    def render():
        UI.header("Trade Reviews", "Calendar, daily trades, review workspace, journal, screenshots and timeline.")
        trades = prepare_trades(AppState.trades())
        screenshots = AppState.screenshots()

        if trades.empty:
            st.warning("No trades found.")
            return

        V4UI.section("Trading Calendar")

        selected_month = CalendarUI.month_selector(trades)

        if selected_month:
            month_trades = CalendarUI.render_month(trades, selected_month)
        else:
            month_trades = trades

        selected_day = st.selectbox(
            "Select trading day",
            sorted(month_trades["date"].astype(str).unique().tolist(), reverse=True)
        )

        selected_trades = month_trades[
            month_trades["date"].astype(str) == selected_day
        ]

        stats = StatisticsEngine.summary(selected_trades)
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Trades", stats["total_trades"])
        c2.metric("Net P/L", FormatEngine.signed_currency(stats["net_profit"]))
        c3.metric("Win Rate", f"{stats['win_rate']}%")
        c4.metric("Profit Factor", stats["profit_factor"])
        c5.metric("Average", FormatEngine.signed_currency(stats["average_trade"]))

        UI.section("Trades")
        st.dataframe(selected_trades, use_container_width=True, hide_index=True, height=320)
        if selected_trades.empty:
            return

        UI.section("Selected Trade Workspace")
        label_map = {}
        for _, row in selected_trades.iterrows():
            label = f"{row.get('ticket')} | {row.get('symbol')} | {row.get('direction')} | {FormatEngine.signed_currency(row.get('net_profit', 0))}"
            label_map[label] = row
        selected = st.selectbox("Select trade", list(label_map.keys()))
        trade = label_map[selected]

        tabs = st.tabs(["Overview", "Analytics", "Review", "Strategy", "Journal", "Screenshots", "Timeline", "Notes", "Charts"])
        with tabs[0]:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Symbol", trade.get("symbol", "-"))
            c2.metric("Direction", trade.get("direction", "-"))
            c3.metric("P/L", FormatEngine.signed_currency(trade.get("net_profit", 0)))
            c4.metric("Volume", trade.get("volume", "-"))
            st.json(trade.to_dict())
        with tabs[1]:
            st.dataframe(pd.DataFrame(trade.to_dict().items(), columns=["Metric", "Value"]), use_container_width=True, hide_index=True)
        with tabs[2]:
            st.text_area("Trade Review", height=220, placeholder="What happened? Did you follow the rules?")
            st.slider("Execution Score", 0, 10, 5)
            st.slider("Confidence", 0, 10, 5)
            st.selectbox("Mistake Type", ["None", "Early Entry", "Late Entry", "Moved Stop", "Revenge Trade", "Overtrading", "Exited Too Early", "Ignored Bias", "Other"])
            st.button("Save Review")
        with tabs[3]:
            st.selectbox("Strategy Used", ["Unassigned", "No Wick Reversal", "FVG Continuation", "Liquidity Sweep", "Break and Retest", "Manual"])
            st.text_area("Strategy Notes", height=180)
        with tabs[4]:
            st.text_area("Journal", height=260)
        with tabs[5]:
            if screenshots is not None and not screenshots.empty:
                st.dataframe(screenshots, use_container_width=True, hide_index=True)
            else:
                st.info("Screenshots linked to this trade will appear here.")
        with tabs[6]:
            st.dataframe(pd.DataFrame([
                {"Stage": "Open", "Time": trade.get("open_time", "-"), "Status": "Completed"},
                {"Stage": "Close", "Time": trade.get("trade_date", "-"), "Status": "Completed"},
                {"Stage": "Review", "Time": "-", "Status": "Waiting"},
            ]), use_container_width=True, hide_index=True)
        with tabs[7]:
            st.text_area("Private Notes", height=240)
        with tabs[8]:
            chart_data = selected_trades.sort_values("trade_date").copy()
            chart_data["day_curve"] = chart_data["net_profit"].cumsum()
            st.line_chart(chart_data.set_index("trade_date")["day_curve"], height=260)
