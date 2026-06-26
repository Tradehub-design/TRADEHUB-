from engine.statistics_engine import StatisticsEngine


class HealthEngine:

    @staticmethod
    def score(trades):

        stats = StatisticsEngine.summary(trades)

        score = 50

        if stats["win_rate"] >= 60:
            score += 15

        if stats["profit_factor"] >= 2:
            score += 15

        if stats["average_trade"] > 0:
            score += 10

        if stats["net_profit"] > 0:
            score += 10

        return min(score, 100)
