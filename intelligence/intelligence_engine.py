import pandas as pd


class IntelligenceEngine:

    @staticmethod
    def analyse(df):

        report = {}

        if df.empty:
            return report

        wins = df[df["net_profit"] > 0]
        losses = df[df["net_profit"] < 0]

        report["total_trades"] = len(df)

        report["win_rate"] = round(
            len(wins) / len(df) * 100,
            2
        )

        report["net_profit"] = round(
            df["net_profit"].sum(),
            2
        )

        if "symbol" in df.columns:

            symbol = (
                df.groupby("symbol")["net_profit"]
                .sum()
                .sort_values(ascending=False)
            )

            report["best_symbol"] = symbol.index[0]
            report["worst_symbol"] = symbol.index[-1]

        if "session" in df.columns:

            session = (
                df.groupby("session")["net_profit"]
                .sum()
                .sort_values(ascending=False)
            )

            report["best_session"] = session.index[0]
            report["worst_session"] = session.index[-1]

        return report
