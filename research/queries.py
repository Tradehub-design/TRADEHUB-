import pandas as pd

from research.filters import ResearchFilters
from research.statistics import ResearchStatistics
from research.comparisons import ResearchComparisons


class ResearchQueries:

    @staticmethod
    def run(
        trades_df,
        symbol="All",
        session="All",
        direction="All",
        result="All",
        start_date=None,
        end_date=None,
        compare_by=None,
    ):

        filtered = ResearchFilters.filter_trades(
            trades_df,
            symbol=symbol,
            session=session,
            direction=direction,
            result=result,
            start_date=start_date,
            end_date=end_date,
        )

        stats = ResearchStatistics.calculate(filtered)

        comparison = pd.DataFrame()

        if compare_by:
            comparison = ResearchComparisons.compare_by_column(
                filtered,
                compare_by
            )

        return filtered, stats, comparison
