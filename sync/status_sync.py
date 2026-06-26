from datetime import datetime

from sync.supabase_sync import SupabaseSync


class StatusSync:

    @staticmethod
    def payload(status, message=""):
        return {
            "id": 1,
            "status": status,
            "message": message,
            "last_sync": datetime.now().isoformat(),
        }

    @staticmethod
    def update(status, message=""):
        SupabaseSync.upsert(
            "sync_status",
            StatusSync.payload(status, message),
            conflict_column="id"
        )
