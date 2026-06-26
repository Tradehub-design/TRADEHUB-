import pandas as pd


class SymbolEngine:

    @staticmethod
    def summary(trades):

        if trades.empty:
            return pd.DataFrame()

        result = (
            trades
            .groupby("symbol")
            .agg(
                Trades=("symbol", "count"),
                NetProfit=("net_profit", "sum"),
                Average=("net_profit", "mean")
            )
            .reset_index()
        )

        result["WinRate"] = (
            trades.groupby("symbol")["net_profit"]
            .apply(lambda x: (x > 0).mean() * 100)
            .values
        ).round(1)

        return result.sort_values(
            "NetProfit",
            ascending=False
        )
