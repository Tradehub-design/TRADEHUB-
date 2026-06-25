class ResearchStats:

    @staticmethod
    def success_rate(results):

        if results.empty:
            return 0

        return round(
            results["worked"].mean() * 100,
            2
        )

    @staticmethod
    def average_follow(results):

        if results.empty:
            return 0

        return round(
            results["follow"].mean(),
            5
        )

    @staticmethod
    def average_adverse(results):

        if results.empty:
            return 0

        return round(
            results["adverse"].mean(),
            5
        )
