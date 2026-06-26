from supabase import create_client

from sync.config import SUPABASE_URL, SUPABASE_KEY
from sync.sync_logger import SyncLogger


class SupabaseSync:

    @staticmethod
    def client():
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise Exception("Missing SUPABASE_URL or SUPABASE_KEY")

        return create_client(SUPABASE_URL, SUPABASE_KEY)

    @staticmethod
    def upsert(table_name, payload, conflict_column=None):
        client = SupabaseSync.client()

        if conflict_column:
            response = (
                client.table(table_name)
                .upsert(payload, on_conflict=conflict_column)
                .execute()
            )
        else:
            response = (
                client.table(table_name)
                .upsert(payload)
                .execute()
            )

        SyncLogger.info(f"Upserted into {table_name}")
        return response
