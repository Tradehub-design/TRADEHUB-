import pandas as pd


class AnalyticsEngine:

    @staticmethod
    def symbol_summary(df):
        if df is None or df.empty:
            return pd.DataFrame()

        if "symbol" not in df.columns or "net_profit" not in df.columns:
            return pd.DataFrame()

        result = (
            df.groupby("symbol")
            .agg(
                Trades=("symbol", "count"),
                NetProfit=("net_profit", "sum"),
                Average=("net_profit", "mean"),
                Wins=("net_profit", lambda x: (x > 0).sum()),
            )
            .reset_index()
        )

        result["WinRate"] = (
            result["Wins"] / result["Trades"] * 100
        ).round(1)

        result["NetProfit"] = result["NetProfit"].round(2)
        result["Average"] = result["Average"].round(2)

        return result.sort_values(
            "NetProfit",
            ascending=False
        )

    @staticmethod
    def session_summary(df):
        if df is None or df.empty:
            return pd.DataFrame()

        if "session" not in df.columns or "net_profit" not in df.columns:
            return pd.DataFrame()

        result = (
            df.groupby("session")
            .agg(
                Trades=("session", "count"),
                NetProfit=("net_profit", "sum"),
                Average=("net_profit", "mean"),
                Wins=("net_profit", lambda x: (x > 0).sum()),
            )
            .reset_index()
        )

        result["WinRate"] = (
            result["Wins"] / result["Trades"] * 100
        ).round(1)

        result["NetProfit"] = result["NetProfit"].round(2)
        result["Average"] = result["Average"].round(2)

        return result.sort_values(
            "NetProfit",
            ascending=False
        )

    @staticmethod
    def monthly_summary(df):
        if df is None or df.empty:
            return pd.DataFrame()

        if "trade_date" not in df.columns or "net_profit" not in df.columns:
            return pd.DataFrame()

        temp = df.copy()

        temp["trade_date"] = pd.to_datetime(
            temp["trade_date"],
            errors="coerce"
        )

        temp = temp.dropna(subset=["trade_date"])

        if temp.empty:
            return pd.DataFrame()

        temp["Month"] = temp["trade_date"].dt.strftime("%Y-%m")

        result = (
            temp.groupby("Month")
            .agg(
                Trades=("Month", "count"),
                NetProfit=("net_profit", "sum"),
                Wins=("net_profit", lambda x: (x > 0).sum()),
            )
            .reset_index()
        )

        result["WinRate"] = (
            result["Wins"] / result["Trades"] * 100
        ).round(1)

        result["NetProfit"] = result["NetProfit"].round(2)

        return result.sort_values("Month")
