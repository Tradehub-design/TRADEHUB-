import pandas as pd

from engine.cache_engine import CacheEngine


class DataEngine:

    @staticmethod
    def _safe_dataframe(df):
        if df is None:
            return pd.DataFrame()

        if isinstance(df, pd.DataFrame):
            return df

        try:
            return pd.DataFrame(df)
        except Exception:
            return pd.DataFrame()

    @staticmethod
    def load_trades():
        return DataEngine._safe_dataframe(
            CacheEngine.trades()
        )

    @staticmethod
    def load_reviews():
        return DataEngine._safe_dataframe(
            CacheEngine.reviews()
        )

    @staticmethod
    def load_screenshots():
        return DataEngine._safe_dataframe(
            CacheEngine.screenshots()
        )

    @staticmethod
    def load_replays():
        return DataEngine._safe_dataframe(
            CacheEngine.replays()
        )
