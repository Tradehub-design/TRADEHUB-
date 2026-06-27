import pandas as pd


class CalendarEngine:

    @staticmethod
    def daily_summary(trades):
        if trades is None or trades.empty:
            return pd.DataFrame()

        if "trade_date" not in trades.columns or "net_profit" not in trades.columns:
            return pd.DataFrame()

        df = trades.copy()
        df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce")
        df = df.dropna(subset=["trade_date"])

        if df.empty:
            return pd.DataFrame()

        df["day"] = df["trade_date"].dt.date

        result = (
            df.groupby("day")
            .agg(
                Trades=("day", "count"),
                NetProfit=("net_profit", "sum"),
                Wins=("net_profit", lambda x: (x > 0).sum()),
                Losses=("net_profit", lambda x: (x < 0).sum()),
            )
            .reset_index()
            .sort_values("day", ascending=False)
        )

        result["WinRate"] = (result["Wins"] / result["Trades"] * 100).round(1)
        result["NetProfit"] = result["NetProfit"].round(2)

        return result
