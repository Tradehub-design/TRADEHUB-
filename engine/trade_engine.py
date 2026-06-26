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
        try:
            Logger.info("Loading trades")

            response = (
                cls._supabase()
                .table("trades")
                .select("*")
                .order("trade_date", desc=True)
                .execute()
            )

            Logger.info(f"Loaded {len(response.data or [])} trades")

            return prepare_trades_dataframe(response.data or [])

        except Exception as e:
            Logger.exception(f"Failed loading trades: {e}")
            return pd.DataFrame()

    @classmethod
    def load_reviews(cls):
        try:
            response = (
                cls._supabase()
                .table("trade_journal_reviews")
                .select("*")
                .execute()
            )

            return pd.DataFrame(response.data or [])

        except Exception as e:
            Logger.exception(f"Failed loading reviews: {e}")
            return pd.DataFrame()

    @classmethod
    def load_screenshots(cls):
        try:
            response = (
                cls._supabase()
                .table("trade_screenshots")
                .select("*")
                .execute()
            )

            return pd.DataFrame(response.data or [])

        except Exception as e:
            Logger.exception(f"Failed loading screenshots: {e}")
            return pd.DataFrame()

    @classmethod
    def load_replays(cls):
        try:
            response = (
                cls._supabase()
                .table("trade_replays")
                .select("*")
                .execute()
            )

            return pd.DataFrame(response.data or [])

        except Exception as e:
            Logger.exception(f"Failed loading replays: {e}")
            return pd.DataFrame()
