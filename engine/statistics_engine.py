import pandas as pd


class StatisticsEngine:

    @staticmethod
    def summary(trades):

        if trades.empty:

            return {

                "total_trades":0,

                "wins":0,

                "losses":0,

                "breakeven":0,

                "win_rate":0,

                "net_profit":0,

                "gross_profit":0,

                "gross_loss":0,

                "profit_factor":0,

                "average_trade":0,

                "average_win":0,

                "average_loss":0

            }

        wins = trades[trades["net_profit"] > 0]

        losses = trades[trades["net_profit"] < 0]

        breakeven = trades[trades["net_profit"] == 0]

        gross_profit = wins["net_profit"].sum()

        gross_loss = abs(losses["net_profit"].sum())

        profit_factor = (
            round(gross_profit / gross_loss, 2)
            if gross_loss > 0
            else 0
        )

        return {

            "total_trades":len(trades),

            "wins":len(wins),

            "losses":len(losses),

            "breakeven":len(breakeven),

            "win_rate":round(
                len(wins) / len(trades) * 100,
                2
            ),

            "net_profit":round(
                trades["net_profit"].sum(),
                2
            ),

            "gross_profit":round(
                gross_profit,
                2
            ),

            "gross_loss":round(
                gross_loss,
                2
            ),

            "profit_factor":profit_factor,

            "average_trade":round(
                trades["net_profit"].mean(),
                2
            ),

            "average_win":round(
                wins["net_profit"].mean(),
                2
            ) if len(wins) else 0,

            "average_loss":round(
                losses["net_profit"].mean(),
                2
            ) if len(losses) else 0

        }
