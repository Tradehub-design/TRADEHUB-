import pandas as pd
import streamlit as st

from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from v2.ui import V2UI


class StrategyBuilderV2:

    @staticmethod
    def _filter_trades(trades, symbol, session, direction):
        df = trades.copy()

        if symbol != "All" and "symbol" in df.columns:
            df = df[df["symbol"] == symbol]

        if session != "All" and "session" in df.columns:
            df = df[df["session"] == session]

        if direction != "Both" and "direction" in df.columns:
            df = df[df["direction"] == direction]

        return df

    @staticmethod
    def _rating(stats):
        score = 0

        if stats["total_trades"] >= 20:
            score += 20
        elif stats["total_trades"] >= 10:
            score += 10

        if stats["win_rate"] >= 60:
            score += 25
        elif stats["win_rate"] >= 50:
            score += 15

        if stats["profit_factor"] >= 2:
            score += 25
        elif stats["profit_factor"] >= 1.2:
            score += 15

        if stats["average_trade"] > 0:
            score += 20

        if stats["net_profit"] > 0:
            score += 10

        if score >= 85:
            return score, "A+"
        if score >= 75:
            return score, "A"
        if score >= 60:
            return score, "B"
        if score >= 45:
            return score, "C"

        return score, "Needs Work"

    @staticmethod
    def render():
        V2UI.header(
            "Strategy Builder",
            "Build, test and rate trading strategies using your trade history."
        )

        trades = DataEngine.load_trades()

        if trades is None or trades.empty:
            st.warning("No trades loaded.")
            return

        if "strategies" not in st.session_state:
            st.session_state["strategies"] = []

        left, right = st.columns([1.1, 2])

        with left:
            V2UI.section("Create Strategy")

            name = st.text_input(
                "Strategy Name",
                placeholder="Example: No Wick Reversal"
            )

            symbols = ["All"]

            if "symbol" in trades.columns:
                symbols += sorted(trades["symbol"].dropna().unique().tolist())

            sessions = ["All"]

            if "session" in trades.columns:
                sessions += sorted(trades["session"].dropna().unique().tolist())

            symbol = st.selectbox("Symbol Filter", symbols)
            session = st.selectbox("Session Filter", sessions)
            direction = st.selectbox("Direction", ["Both", "BUY", "SELL"])

            entry_type = st.selectbox(
                "Entry Type",
                [
                    "Manual",
                    "Reversal",
                    "Continuation",
                    "Liquidity Sweep",
                    "FVG",
                    "Break and Retest",
                    "No Wick Reversal",
                ]
            )

            target_rr = st.number_input(
                "Target R:R",
                min_value=0.0,
                max_value=20.0,
                value=2.0,
                step=0.1,
            )

            rules = st.text_area(
                "Rules",
                placeholder="Example: Only trade after liquidity sweep. No entries during high impact news.",
                height=160,
            )

            checklist = st.text_area(
                "Checklist",
                placeholder="Example:\n- HTF bias confirmed\n- Entry candle confirmed\n- Stop placed beyond structure",
                height=160,
            )

            if st.button("Save Strategy"):
                if not name:
                    st.error("Strategy name is required.")
                else:
                    st.session_state["strategies"].append({
                        "name": name,
                        "symbol": symbol,
                        "session": session,
                        "direction": direction,
                        "entry_type": entry_type,
                        "target_rr": target_rr,
                        "rules": rules,
                        "checklist": checklist,
                    })

                    st.success("Strategy saved.")

        with right:
            V2UI.section("Strategy Backtest")

            preview_name = name or "Current Strategy"

            filtered = StrategyBuilderV2._filter_trades(
                trades,
                symbol,
                session,
                direction,
            )

            stats = StatisticsEngine.summary(filtered)
            score, grade = StrategyBuilderV2._rating(stats)

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric("Trades", stats["total_trades"])
            c2.metric("Net P/L", FormatEngine.signed_currency(stats["net_profit"]))
            c3.metric("Win Rate", f"{stats['win_rate']}%")
            c4.metric("Profit Factor", stats["profit_factor"])
            c5.metric("Rating", grade)

            st.progress(score / 100)

            st.caption(f"{preview_name} score: {score}/100")

            V2UI.section("Matching Trades")

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True,
                height=420,
            )

        V2UI.section("Saved Strategies")

        if not st.session_state["strategies"]:
            st.info("No saved strategies yet.")
        else:
            strategy_df = pd.DataFrame(st.session_state["strategies"])

            st.dataframe(
                strategy_df,
                use_container_width=True,
                hide_index=True,
            )
