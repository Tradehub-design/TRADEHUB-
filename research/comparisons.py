import pandas as pd
from research.statistics import ResearchStatistics


class ResearchComparisons:

    @staticmethod
    def compare_by_column(df, column):
        if df.empty or column not in df.columns:
            return pd.DataFrame()

        rows = []

        for value in sorted(df[column].dropna().unique()):
            subset = df[df[column] == value]
            stats = ResearchStatistics.calculate(subset)

            rows.append({
                column: value,
                "trades": stats["total_trades"],
                "net_profit": stats["net_profit"],
                "win_rate": stats["win_rate"],
                "profit_factor": stats["profit_factor"],
                "expectancy": stats["expectancy"],
            })

        return pd.DataFrame(rows).sort_values("net_profit", ascending=False)
