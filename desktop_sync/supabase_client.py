from supabase import create_client

from desktop_sync.config import DesktopSyncConfig


class DesktopSupabaseClient:

    @staticmethod
    def client():
        if not DesktopSyncConfig.SUPABASE_URL:
            raise Exception("SUPABASE_URL is missing")

        if not DesktopSyncConfig.SUPABASE_KEY:
            raise Exception("SUPABASE_KEY is missing")

        return create_client(
            DesktopSyncConfig.SUPABASE_URL,
            DesktopSyncConfig.SUPABASE_KEY
        )

    @staticmethod
    def upsert(table_name, payload, conflict_column=None):
        client = DesktopSupabaseClient.client()

        if conflict_column:
            return (
                client.table(table_name)
                .upsert(payload, on_conflict=conflict_column)
                .execute()
            )

        return (
            client.table(table_name)
            .upsert(payload)
            .execute()
        )

    @staticmethod
    def insert(table_name, payload):
        return (
            DesktopSupabaseClient.client()
            .table(table_name)
            .insert(payload)
            .execute()
        )
