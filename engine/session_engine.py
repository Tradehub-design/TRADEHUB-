import pandas as pd


class SessionEngine:

    @staticmethod
    def summary(trades):

        if trades.empty:
            return pd.DataFrame()

        if "session" not in trades.columns:
            return pd.DataFrame()

        result = (
            trades
            .groupby("session")
            .agg(
                Trades=("session", "count"),
                NetProfit=("net_profit", "sum"),
                Average=("net_profit", "mean")
            )
            .reset_index()
        )

        result["WinRate"] = (
            trades.groupby("session")["net_profit"]
            .apply(lambda x: (x > 0).mean() * 100)
            .values
        ).round(1)

        return result.sort_values(
            "NetProfit",
            ascending=False
        )
