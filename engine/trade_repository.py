from engine.cache_engine import CacheEngine


class TradeRepository:

    @staticmethod
    def all():

        return CacheEngine.trades()

    @staticmethod
    def trade(ticket):

        trades = CacheEngine.trades()

        if trades.empty:
            return None

        trade = trades[
            trades["ticket"] == ticket
        ]

        if trade.empty:
            return None

        return trade.iloc[0]

    @staticmethod
    def reviews():

        return CacheEngine.reviews()

    @staticmethod
    def screenshots():

        return CacheEngine.screenshots()

    @staticmethod
    def replays():

        return CacheEngine.replays()
