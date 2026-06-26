import pandas as pd


class AnalyticsEngine:

    @staticmethod
    def symbol_summary(df):

        if df.empty:
            return pd.DataFrame()

        result = (
            df.groupby("symbol")
            .agg(
                Trades=("symbol", "count"),
                NetProfit=("net_profit", "sum"),
                Average=("net_profit", "mean"),
                Wins=("net_profit", lambda x: (x > 0).sum())
            )
            .reset_index()
        )

        result["WinRate"] = (
            result["Wins"] / result["Trades"] * 100
        ).round(1)

        return result.sort_values(
            "NetProfit",
            ascending=False
        )

    @staticmethod
    def session_summary(df):

        if "session" not in df.columns:
            return pd.DataFrame()

        result = (
            df.groupby("session")
            .agg(
                Trades=("session", "count"),
                NetProfit=("net_profit", "sum"),
                Average=("net_profit", "mean"),
                Wins=("net_profit", lambda x: (x > 0).sum())
            )
            .reset_index()
        )

        result["WinRate"] = (
            result["Wins"] / result["Trades"] * 100
        ).round(1)

        return result.sort_values(
            "NetProfit",
            ascending=False
        )

    @staticmethod
    def monthly_summary(df):

        if "trade_date" not in df.columns:
            return pd.DataFrame()

        temp = df.copy()

        temp["Month"] = pd.to_datetime(
            temp["trade_date"]
        ).dt.strftime("%Y-%m")

        return (
            temp.groupby("Month")
            .agg(
                Trades=("Month", "count"),
                NetProfit=("net_profit", "sum")
            )
            .reset_index()
        )
