import pandas as pd
import streamlit as st
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from tradehub_v4.core.state import AppState
from tradehub_v4.core.ui import UI


class StrategiesWorkspace:
    @staticmethod
    def rating(stats):
        score = 0
        score += 20 if stats["total_trades"] >= 20 else 10 if stats["total_trades"] >= 10 else 0
        score += 25 if stats["win_rate"] >= 60 else 15 if stats["win_rate"] >= 50 else 0
        score += 25 if stats["profit_factor"] >= 2 else 15 if stats["profit_factor"] >= 1.2 else 0
        score += 20 if stats["average_trade"] > 0 else 0
        score += 10 if stats["net_profit"] > 0 else 0
        grade = "A+" if score >= 85 else "A" if score >= 75 else "B" if score >= 60 else "C" if score >= 45 else "Needs Work"
        return score, grade

    @staticmethod
    def render():
        UI.header("Strategies", "Build, filter and score strategy ideas using trade history.")
        trades = AppState.trades()
        if trades is None or trades.empty:
            st.warning("No trades found.")
            return
        left, right = st.columns([1.1, 2])
        with left:
            UI.section("Build Strategy")
            name = st.text_input("Strategy Name", placeholder="No Wick Reversal")
            symbols = ["All"] + sorted(trades["symbol"].dropna().unique().tolist()) if "symbol" in trades.columns else ["All"]
            sessions = ["All"] + sorted(trades["session"].dropna().unique().tolist()) if "session" in trades.columns else ["All"]
            symbol = st.selectbox("Symbol", symbols)
            session = st.selectbox("Session", sessions)
            direction = st.selectbox("Direction", ["Both", "BUY", "SELL"])
            entry_type = st.selectbox("Entry Type", ["Manual", "Reversal", "Continuation", "Liquidity Sweep", "FVG", "Break and Retest", "No Wick Reversal"])
            st.number_input("Target R:R", min_value=0.0, max_value=20.0, value=2.0, step=0.1)
            st.text_area("Rules", height=160)
            st.text_area("Checklist", height=160)
        with right:
            df = trades.copy()
            if symbol != "All" and "symbol" in df.columns: df = df[df["symbol"] == symbol]
            if session != "All" and "session" in df.columns: df = df[df["session"] == session]
            if direction != "Both" and "direction" in df.columns: df = df[df["direction"] == direction]
            stats = StatisticsEngine.summary(df)
            score, grade = StrategiesWorkspace.rating(stats)
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Trades", stats["total_trades"])
            c2.metric("Net P/L", FormatEngine.signed_currency(stats["net_profit"]))
            c3.metric("Win Rate", f"{stats['win_rate']}%")
            c4.metric("Profit Factor", stats["profit_factor"])
            c5.metric("Rating", grade)
            st.progress(score / 100)
            st.caption(f"{name or 'Current strategy'} score: {score}/100")
            st.dataframe(df, use_container_width=True, hide_index=True, height=420)
