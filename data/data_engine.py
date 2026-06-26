import pandas as pd

from engine.cache_engine import CacheEngine
from data.real_trades_seed import load_real_trades
from data.real_trades_seed_extra import load_extra_real_trades


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
    def _real_seed_data():
        first = load_real_trades()
        extra = load_extra_real_trades()

        combined = pd.concat(
            [first, extra],
            ignore_index=True
        )

        combined = combined.drop_duplicates(
            subset=["ticket"],
            keep="last"
        )

        return combined.sort_values(
            "trade_date",
            ascending=False
        )

    @staticmethod
    def _use_seed_if_needed(df):
        df = DataEngine._safe_dataframe(df)

        if df.empty:
            return DataEngine._real_seed_data()

        if len(df) <= 1:
            return DataEngine._real_seed_data()

        return df

    @staticmethod
    def load_trades():
        return DataEngine._use_seed_if_needed(
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

    @staticmethod
    def load_account_snapshot():
        return DataEngine._safe_dataframe(
            CacheEngine.account_snapshot()
        )

    @staticmethod
    def load_open_positions():
        return DataEngine._safe_dataframe(
            CacheEngine.open_positions()
        )

    @staticmethod
    def load_sync_status():
        return DataEngine._safe_dataframe(
            CacheEngine.sync_status()
        )
