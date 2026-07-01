import streamlit as st
import pandas as pd


class CalendarUI:

    @staticmethod
    def render(trades):
        st.caption("Calendar summary by trading day")

        if trades is None or trades.empty:
            st.info("No trades available for calendar.")
            return

        df = trades.copy()

        if "date" not in df.columns:
            if "open_time" in df.columns:
                df["date"] = pd.to_datetime(df["open_time"], errors="coerce").dt.date
            elif "trade_date" in df.columns:
                df["date"] = pd.to_datetime(df["trade_date"], errors="coerce").dt.date
            else:
                st.warning("No date, open_time, or trade_date column found.")
                return

        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df = df.dropna(subset=["date"])

        pnl_col = None
        for col in ["net_profit", "profit", "pnl", "Profit"]:
            if col in df.columns:
                pnl_col = col
                break

        if pnl_col:
            daily = (
                df.groupby("date")
                .agg(
                    trades=("date", "count"),
                    pnl=(pnl_col, "sum"),
                )
                .reset_index()
                .sort_values("date", ascending=False)
            )

            daily["pnl"] = daily["pnl"].round(2)
            daily["result"] = daily["pnl"].apply(
                lambda x: "Win Day" if x > 0 else "Loss Day" if x < 0 else "Breakeven"
            )
        else:
            daily = (
                df.groupby("date")
                .agg(trades=("date", "count"))
                .reset_index()
                .sort_values("date", ascending=False)
            )
            daily["pnl"] = 0
            daily["result"] = "No P/L column"

        c1, c2, c3, c4 = st.columns(4)

        total_days = len(daily)
        total_trades = int(daily["trades"].sum())
        total_pnl = float(daily["pnl"].sum()) if "pnl" in daily.columns else 0
        win_days = int((daily["pnl"] > 0).sum()) if "pnl" in daily.columns else 0

        c1.metric("Trading Days", total_days)
        c2.metric("Total Trades", total_trades)
        c3.metric("Total P/L", round(total_pnl, 2))
        c4.metric("Win Days", win_days)

        st.dataframe(
            daily,
            width="stretch",
            hide_index=True,
        )

    @staticmethod
    def show(trades):
        CalendarUI.render(trades)
