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
            "Weekdays",
            "Months",
            "Hours",
            "Drawdown",
            "Risk",
            "Accounts",
        ])

        with tabs[0]:
            V2UI.section("Performance Overview")
            AnalyticsV2._summary_cards(df)

            V2UI.section("Equity Curve")
            curve = AnalyticsV2._drawdown(df)

            if not curve.empty:
                st.line_chart(
                    curve.set_index("trade_date")["equity_curve"],
                    height=300
                )

            V2UI.section("Monthly Performance")
            monthly = AnalyticsEngine.monthly_summary(df)

            if not monthly.empty:
                st.bar_chart(
                    monthly.set_index("Month")["NetProfit"],
                    height=280
                )

            V2UI.section("Trade History")
            st.dataframe(
                df.head(50),
                use_container_width=True,
                hide_index=True
            )

        with tabs[1]:
            V2UI.section("Symbol Analytics")
            symbol_summary = AnalyticsEngine.symbol_summary(df)

            st.dataframe(
                symbol_summary,
                use_container_width=True,
                hide_index=True
            )

            if not symbol_summary.empty:
                st.bar_chart(
                    symbol_summary.set_index("symbol")["NetProfit"],
                    height=320
                )

        with tabs[2]:
            V2UI.section("Session Analytics")
            session_summary = AnalyticsEngine.session_summary(df)

            st.dataframe(
                session_summary,
                use_container_width=True,
                hide_index=True
            )

            if not session_summary.empty:
                st.bar_chart(
                    session_summary.set_index("session")["NetProfit"],
                    height=320
                )

        with tabs[3]:
            V2UI.section("Weekday Analytics")
            weekday_summary = AnalyticsV2._group_summary(df, "weekday")

            st.dataframe(
                weekday_summary,
                use_container_width=True,
                hide_index=True
            )

            if not weekday_summary.empty:
                st.bar_chart(
                    weekday_summary.set_index("weekday")["NetProfit"],
                    height=320
                )

        with tabs[4]:
            V2UI.section("Month Analytics")
            month_summary = AnalyticsV2._group_summary(df, "month")

            st.dataframe(
                month_summary,
                use_container_width=True,
                hide_index=True
            )

            if not month_summary.empty:
                st.bar_chart(
                    month_summary.set_index("month")["NetProfit"],
                    height=320
                )

        with tabs[5]:
            V2UI.section("Hour Analytics")
            hour_summary = AnalyticsV2._group_summary(df, "hour")

            st.dataframe(
                hour_summary,
                use_container_width=True,
                hide_index=True
            )

            if not hour_summary.empty:
                st.bar_chart(
                    hour_summary.set_index("hour")["NetProfit"],
                    height=320
                )

        with tabs[6]:
            V2UI.section("Drawdown")
            drawdown = AnalyticsV2._drawdown(df)

            if drawdown.empty:
                st.info("No drawdown data.")
            else:
                st.line_chart(
                    drawdown.set_index("trade_date")["drawdown"],
                    height=320
                )

                max_dd = drawdown["drawdown"].min()

                st.metric(
                    "Max Drawdown",
                    FormatEngine.signed_currency(max_dd)
                )

                st.dataframe(
                    drawdown[
                        [
                            "ticket",
                            "trade_date",
                            "symbol",
                            "direction",
                            "net_profit",
                            "equity_curve",
                            "drawdown",
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True
                )

        with tabs[7]:
            V2UI.section("Risk Analytics")

            stats = StatisticsEngine.summary(df)

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Average Win", FormatEngine.signed_currency(stats["average_win"]))
            c2.metric("Average Loss", FormatEngine.signed_currency(stats["average_loss"]))
            c3.metric("Gross Profit", FormatEngine.currency(stats["gross_profit"]))
            c4.metric("Gross Loss", FormatEngine.currency(stats["gross_loss"]))

            if "hold_minutes" in df.columns:
                V2UI.section("Holding Time")
                hold = df["hold_minutes"].dropna()

                if not hold.empty:
                    st.metric("Average Hold Minutes", round(hold.mean(), 1))
                    st.bar_chart(hold)

        with tabs[8]:
            V2UI.section("Account Comparison")

            if "account_number" not in df.columns:
                st.info("No account data available.")
            else:
                account_summary = AnalyticsV2._group_summary(
                    df,
                    "account_number"
                )

                st.dataframe(
                    account_summary,
                    use_container_width=True,
                    hide_index=True
                )
