import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe


class DataEngine:

    @staticmethod
    def load_trades():

        supabase = get_supabase_client()

        response = (
            supabase.table("trades")
            .select("*")
            .order("trade_date", desc=True)
            .execute()
        )

        return prepare_trades_dataframe(response.data)

    @staticmethod
    def load_reviews():

        supabase = get_supabase_client()

        response = (
            supabase.table("trade_journal_reviews")
            .select("*")
            .execute()
        )

        return pd.DataFrame(response.data)

    @staticmethod
    def load_screenshots():

        supabase = get_supabase_client()

        response = (
            supabase.table("trade_screenshots")
            .select("*")
            .execute()
        )

        return pd.DataFrame(response.data)

    @staticmethod
    def load_daily_plan():

        supabase = get_supabase_client()

        response = (
            supabase.table("daily_plans")
            .select("*")
            .order("plan_date", desc=True)
            .limit(1)
            .execute()
        )

        return pd.DataFrame(response.data)

    @staticmethod
    def load_playbooks():

        supabase = get_supabase_client()

        response = (
            supabase.table("playbooks")
            .select("*")
            .execute()
        )

        return pd.DataFrame(response.data)
