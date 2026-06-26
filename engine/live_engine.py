import pandas as pd

from utils.supabase_client import get_supabase_client


class LiveEngine:

    @staticmethod
    def account_snapshot():
        try:
            response = (
                get_supabase_client()
                .table("account_snapshots")
                .select("*")
                .execute()
            )

            return pd.DataFrame(response.data or [])

        except Exception:
            return pd.DataFrame()

    @staticmethod
    def open_positions():
        try:
            response = (
                get_supabase_client()
                .table("open_positions")
                .select("*")
                .order("synced_at", desc=True)
                .execute()
            )

            return pd.DataFrame(response.data or [])

        except Exception:
            return pd.DataFrame()

    @staticmethod
    def sync_status():
        try:
            response = (
                get_supabase_client()
                .table("sync_status")
                .select("*")
                .eq("id", 1)
                .execute()
            )

            return pd.DataFrame(response.data or [])

        except Exception:
            return pd.DataFrame()
