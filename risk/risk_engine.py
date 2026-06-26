class RiskEngine:

    @staticmethod
    def calculate(trades):
        if trades is None or trades.empty or "net_profit" not in trades.columns:
            return {
                "daily": 0,
                "weekly": 0,
                "monthly": 0,
                "largest_loss": 0,
                "largest_win": 0,
                "average_loss": 0,
                "average_win": 0,
            }

        wins = trades[trades["net_profit"] > 0]
        losses = trades[trades["net_profit"] < 0]

        return {
            "daily": round(trades.tail(10)["net_profit"].sum(), 2),
            "weekly": round(trades.tail(40)["net_profit"].sum(), 2),
            "monthly": round(trades.tail(150)["net_profit"].sum(), 2),
            "largest_loss": round(trades["net_profit"].min(), 2),
            "largest_win": round(trades["net_profit"].max(), 2),
            "average_loss": round(losses["net_profit"].mean(), 2) if not losses.empty else 0,
            "average_win": round(wins["net_profit"].mean(), 2) if not wins.empty else 0,
        }
