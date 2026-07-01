import streamlit as st
from tradehub_v4.core.state import AppState
from tradehub_v4.core.ui import UI


class ResearchAIWorkspace:
    @staticmethod
    def render():
        UI.header("Research & AI", "Trading plans, market research, psychology and AI coach.")
        tabs = st.tabs(["Weekly Plan", "Research", "Market Bias", "Psychology", "AI Coach"])
        with tabs[0]:
            UI.section("Weekly Trading Plan")
            st.text_input("Week Beginning")
            st.text_area("Objectives", height=160)
            st.text_area("Markets To Watch", height=160)
            st.text_area("Important News", height=130)
        with tabs[1]:
            UI.section("Market Research")
            st.text_area("Research Notes", height=330)
            st.file_uploader("Attach screenshots", accept_multiple_files=True)
        with tabs[2]:
            UI.section("Market Bias")
            cols = st.columns(3)
            for i, pair in enumerate(["EURUSD", "GBPUSD", "USDJPY", "USDCAD", "GBPNZD", "XAUUSD"]):
                with cols[i % 3]:
                    st.selectbox(pair, ["Bullish", "Bearish", "Neutral"], key=f"bias_{pair}")
        with tabs[3]:
            UI.section("Psychology")
            st.slider("Confidence", 1, 10, 5)
            st.slider("Stress", 1, 10, 5)
            st.slider("Discipline", 1, 10, 5)
            st.text_area("Daily Reflection", height=240)
        with tabs[4]:
            trades = AppState.trades()
            if trades is not None and not trades.empty:
                c1, c2 = st.columns(2)
                c1.metric("Winning Trades", len(trades[trades["net_profit"] > 0]))
                c2.metric("Losing Trades", len(trades[trades["net_profit"] < 0]))
            st.info("AI Coach foundation: connects to your trades, reviews, strategies and journal notes in the next AI phase.")
            st.text_area("Ask AI", placeholder="What should I focus on this week?")
            st.button("Analyse")
