import streamlit as st
import pandas as pd

from data.data_engine import DataEngine
from v2.ui import V2UI


class ResearchAIV2:

    @staticmethod
    def render():

        V2UI.header(
            "Research & AI",
            "Trading plans, market research and AI coaching."
        )

        tabs = st.tabs([
            "Weekly Plan",
            "Research",
            "Market Bias",
            "Psychology",
            "AI Coach"
        ])

        with tabs[0]:

            V2UI.section("Weekly Trading Plan")

            st.text_input("Week Beginning")

            st.text_area(
                "Objectives",
                height=180
            )

            st.text_area(
                "Markets To Watch",
                height=180
            )

            st.text_area(
                "Important News",
                height=160
            )

            st.button("Save Weekly Plan")

        with tabs[1]:

            V2UI.section("Market Research")

            st.text_area(
                "Research Notes",
                height=350
            )

            st.file_uploader(
                "Attach screenshots",
                accept_multiple_files=True
            )

        with tabs[2]:

            V2UI.section("Market Bias")

            cols = st.columns(4)

            pairs = [
                "EURUSD",
                "GBPUSD",
                "USDJPY",
                "USDCAD",
                "GBPNZD",
                "XAUUSD"
            ]

            for i, pair in enumerate(pairs):

                with cols[i % 4]:

                    st.selectbox(
                        pair,
                        [
                            "Bullish",
                            "Bearish",
                            "Neutral"
                        ],
                        key=pair
                    )

        with tabs[3]:

            V2UI.section("Psychology")

            st.slider(
                "Confidence",
                1,
                10,
                5
            )

            st.slider(
                "Stress",
                1,
                10,
                5
            )

            st.slider(
                "Discipline",
                1,
                10,
                5
            )

            st.text_area(
                "Daily Reflection",
                height=250
            )

        with tabs[4]:

            V2UI.section("AI Coach")

            trades = DataEngine.load_trades()

            if trades is None or trades.empty:

                st.info("No trade data available.")

            else:

                winners = len(trades[trades["net_profit"] > 0])
                losers = len(trades[trades["net_profit"] < 0])

                st.metric("Winning Trades", winners)
                st.metric("Losing Trades", losers)

                st.info(
                    "AI coaching engine will analyse your journals, reviews, strategies and trading statistics in a later phase."
                )

                st.text_area(
                    "Ask AI",
                    placeholder="Why did I lose money this week?"
                )

                st.button("Analyse")
