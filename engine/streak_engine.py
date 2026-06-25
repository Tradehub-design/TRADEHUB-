class StreakEngine:

    @staticmethod
    def calculate(df):

        if df.empty:
            return {
                "current":0,
                "best":0
            }

        current = 0
        best = 0

        for pnl in df["net_profit"]:

            if pnl > 0:
                current += 1
                best = max(best,current)
            else:
                current = 0

        return {
            "current":current,
            "best":best
        }
