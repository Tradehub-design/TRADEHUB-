import pandas as pd
import streamlit as st

from data.data_engine import DataEngine
from engine.calendar_engine import CalendarEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from v2.ui import V2UI


class TradeReviewV2:

    @staticmethod
    def render():
        V2UI.header(
            "Trade Review",
            "Calendar, daily trades, journal, screenshots, timeline and notes."
        )

        trades = DataEngine.load_trades()

        if trades is None or trades.empty:
            st.warning("No trades loaded.")
            return

        trades = trades.copy()
        trades["trade_date"] = pd.to_datetime(
            trades["trade_date"],
            errors="coerce"
        )

        daily = CalendarEngine.daily_summary(trades)

        V2UI.section("Trading Calendar")

        if daily.empty:
            st.info("No valid calendar data.")
            selected_trades = trades
        else:
            st.dataframe(
                daily,
                use_container_width=True,
                hide_index=True,
                height=280,
            )

            selected_day = st.selectbox(
                "Select trading day",
                daily["day"].astype(str).tolist()
            )

            selected_trades = trades[
                trades["trade_date"].astype(str).str.startswith(selected_day)
            ]

        stats = StatisticsEngine.summary(selected_trades)

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Trades", stats["total_trades"])
        c2.metric("Net P/L", FormatEngine.signed_currency(stats["net_profit"]))
        c3.metric("Win Rate", f"{stats['win_rate']}%")
        c4.metric("Profit Factor", stats["profit_factor"])
        c5.metric("Avg Trade", FormatEngine.signed_currency(stats["average_trade"]))

        V2UI.section("Trades For Selected Day")

        st.dataframe(
            selected_trades,
            use_container_width=True,
            hide_index=True,
            height=340,
        )

        if selected_trades.empty:
            st.stop()

        V2UI.section("Selected Trade Workspace")

        ticket = st.selectbox(
            "Select trade",
            selected_trades["ticket"].tolist()
        )

        trade = selected_trades[
            selected_trades["ticket"] == ticket
        ].iloc[0]

        tabs = st.tabs([
            "Overview",
            "Analytics",
            "Review",
            "Strategy",
            "Journal",
            "Screenshots",
            "Timeline",
            "Notes",
            "Charts",
        ])

        with tabs[0]:
            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Symbol", trade.get("symbol", "-"))
            c2.metric("Direction", trade.get("direction", "-"))
            c3.metric("P/L", FormatEngine.signed_currency(trade.get("net_profit", 0)))
            c4.metric("Volume", trade.get("volume", "-"))

            st.json(trade.to_dict())

        with tabs[1]:
            st.write("Trade-level analytics")

            analytics_table = {
                "Entry Price": trade.get("entry_price"),
                "Exit Price": trade.get("exit_price"),
                "Open Time": trade.get("open_time"),
                "Close Time": trade.get("trade_date"),
                "Session": trade.get("session"),
                "Commission": trade.get("commission"),
                "Swap": trade.get("swap"),
            }

            st.dataframe(
                pd.DataFrame(
                    analytics_table.items(),
                    columns=["Metric", "Value"]
                ),
                use_container_width=True,
                hide_index=True,
            )

        with tabs[2]:
            st.text_area(
                "Trade Review",
                placeholder="What happened? Was this a valid setup? Did you follow your rules?",
                height=220,
            )

            st.slider("Execution Score", 0, 10, 5)
            st.slider("Confidence", 0, 10, 5)

            st.selectbox(
                "Mistake Type",
                [
                    "None",
                    "Early Entry",
                    "Late Entry",
                    "Moved Stop",
                    "Revenge Trade",
                    "Overtrading",
                    "Exited Too Early",
                    "Ignored Bias",
                    "Other",
                ],
            )

            st.button("Save Review")

        with tabs[3]:
            st.selectbox(
                "Strategy Used",
                [
                    "Unassigned",
                    "No Wick Reversal",
                    "FVG Continuation",
                    "Liquidity Sweep",
                    "Break and Retest",
                    "Manual",
                ],
            )

            st.text_area("Strategy Notes", height=180)

        with tabs[4]:
            st.text_area(
                "Journal",
                placeholder="Write your trade journal here.",
                height=260,
            )

        with tabs[5]:
            st.info("Screenshots linked to this trade will appear here.")

        with tabs[6]:
            timeline = pd.DataFrame([
                {
                    "Stage": "Open",
                    "Time": trade.get("open_time", "-"),
                    "Status": "Completed",
                },
                {
                    "Stage": "Close",
                    "Time": trade.get("trade_date", "-"),
                    "Status": "Completed",
                },
                {
                    "Stage": "Review",
                    "Time": "-",
                    "Status": "Waiting",
                },
            ])

            st.dataframe(
                timeline,
                use_container_width=True,
                hide_index=True,
            )

        with tabs[7]:
            st.text_area("Private Notes", height=240)

        with tabs[8]:
            chart_data = selected_trades.copy()
            chart_data = chart_data.sort_values("trade_date")
            chart_data["day_curve"] = chart_data["net_profit"].cumsum()

            st.line_chart(
                chart_data.set_index("trade_date")["day_curve"],
                height=260,
            )
