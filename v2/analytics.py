import pandas as pd
import streamlit as st

from data.data_engine import DataEngine
from engine.analytics_engine import AnalyticsEngine
from engine.statistics_engine import StatisticsEngine
from engine.format_engine import FormatEngine
from v2.ui import V2UI


class AnalyticsV2:

    @staticmethod
    def _prepare(trades):
        df = trades.copy()

        df["trade_date"] = pd.to_datetime(
            df["trade_date"],
            errors="coerce"
        )

        df["weekday"] = df["trade_date"].dt.day_name()
        df["month"] = df["trade_date"].dt.strftime("%Y-%m")
        df["hour"] = df["trade_date"].dt.hour

        if "open_time" in df.columns:
            df["open_time_dt"] = pd.to_datetime(
                df["open_time"],
                errors="coerce"
            )

            df["hold_minutes"] = (
                df["trade_date"] - df["open_time_dt"]
            ).dt.total_seconds() / 60

        return df

    @staticmethod
    def _summary_cards(trades):
        stats = StatisticsEngine.summary(trades)

        c1, c2, c3, c4, c5, c6 = st.columns(6)

        c1.metric("Trades", stats["total_trades"])
        c2.metric("Net P/L", FormatEngine.signed_currency(stats["net_profit"]))
        c3.metric("Win Rate", f"{stats['win_rate']}%")
        c4.metric("Profit Factor", stats["profit_factor"])
        c5.metric("Avg Trade", FormatEngine.signed_currency(stats["average_trade"]))
        c6.metric("Largest Loss", FormatEngine.signed_currency(stats["average_loss"]))

    @staticmethod
    def _group_summary(df, group_col):
        if df is None or df.empty:
            return pd.DataFrame()

        if group_col not in df.columns:
            return pd.DataFrame()

        result = (
            df.groupby(group_col)
            .agg(
                Trades=(group_col, "count"),
                NetProfit=("net_profit", "sum"),
                Average=("net_profit", "mean"),
                Wins=("net_profit", lambda x: (x > 0).sum()),
                Losses=("net_profit", lambda x: (x < 0).sum()),
            )
            .reset_index()
        )

        result["WinRate"] = (
            result["Wins"] / result["Trades"] * 100
        ).round(1)

        result["NetProfit"] = result["NetProfit"].round(2)
        result["Average"] = result["Average"].round(2)

        return result.sort_values("NetProfit", ascending=False)

    @staticmethod
    def _drawdown(df):
        if df is None or df.empty:
            return pd.DataFrame()

        temp = df.copy()
        temp = temp.dropna(subset=["trade_date"])
        temp = temp.sort_values("trade_date")

        temp["equity_curve"] = temp["net_profit"].cumsum()
        temp["peak"] = temp["equity_curve"].cummax()
        temp["drawdown"] = temp["equity_curve"] - temp["peak"]

        return temp

    @staticmethod
    def render():
        V2UI.header(
            "Analytics",
            "Overview, symbols, sessions, months, drawdown and risk."
        )

        trades = DataEngine.load_trades()

        if trades is None or trades.empty:
            st.warning("No trades loaded.")
            return

        df = AnalyticsV2._prepare(trades)

        tabs = st.tabs([
            "Overview",
            "Symbols",
            "Sessions",
           
