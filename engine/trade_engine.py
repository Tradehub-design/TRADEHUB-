import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe

from core.logger import Logger


class TradeEngine:

    @staticmethod
    def _supabase():
        return get_supabase_client()

    @classmethod
    def load_all(cls):

        Logger.info("Loading trades")

        response = (
            cls._supabase()
            .table("trades")
            .select("*")
            .order("trade_date", desc=True)
            .execute()
        )

        Logger.info(
            f"Loaded {len(response.data)} trades"
        )

        return prepare_trades_dataframe(
            response.data
        )

    @classmethod
    def load_reviews(cls):

        Logger.info("Loading reviews")

        response = (
            cls._supabase()
            .table("trade_journal_reviews")
            .select("*")
            .execute()
        )

        return pd.DataFrame(response.data)

    @classmethod
    def load_screenshots(cls):

        Logger.info("Loading screenshots")

        response = (
            cls._supabase()
            .table("trade_screenshots")
            .select("*")
            .execute()
        )

        return pd.DataFrame(response.data)

    @classmethod
    def load_replays(cls):

        Logger.info("Loading replays")

        response = (
            cls._supabase()
            .table("trade_replays")
            .select("*")
            .execute()
        )

        return pd.DataFrame(response.data)
