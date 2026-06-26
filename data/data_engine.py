from engine.cache_engine import CacheEngine


class DataEngine:

    @staticmethod
    def load_trades():
        return CacheEngine.trades()

    @staticmethod
    def load_reviews():
        return CacheEngine.reviews()

    @staticmethod
    def load_screenshots():
        return CacheEngine.screenshots()

    @staticmethod
    def load_replays():
        return CacheEngine.replays()
