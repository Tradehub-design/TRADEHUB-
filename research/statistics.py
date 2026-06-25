class ResearchStatistics:

    @staticmethod
    def calculate(df):
        if df.empty or "net_profit" not in df.columns:
            return {
                "total_trades": 0,
                "net_profit": 0,
                "win_rate": 0,
                "average_win": 0,
                "average_loss": 0,
                "profit_factor": 0,
                "expectancy": 0,
            }

        wins = df[df["net_profit"] > 0]
        losses = df[df["net_profit"] < 0]

        total = len(df)
        gross_profit = wins["net_profit"].sum() if not wins.empty else 0
        gross_loss = abs(losses["net_profit"].sum()) if not losses.empty else 0

        avg_win = wins["net_profit"].mean() if not wins.empty else 0
        avg_loss = losses["net_profit"].mean() if not losses.empty else 0

        win_rate = len(wins) / total if total else 0
        loss_rate = len(losses) / total if total else 0

        expectancy = (avg_win * win_rate) + (avg_loss * loss_rate)

        return {
            "total_trades": total,
            "net_profit": round(df["net_profit"].sum(), 2),
            "win_rate": round(win_rate * 100, 2),
            "average_win": round(avg_win, 2),
            "average_loss": round(avg_loss, 2),
            "profit_factor": round(gross_profit / gross_loss, 2) if gross_loss else 0,
            "expectancy": round(expectancy, 2),
        }
