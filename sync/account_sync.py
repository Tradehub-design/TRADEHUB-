from datetime import datetime

from sync.config import BROKER_NAME, ACCOUNT_CURRENCY
from sync.mt5_connector import MT5Connector
from sync.supabase_sync import SupabaseSync


class AccountSync:

    @staticmethod
    def build_payload(account):
        return {
            "account_number": str(account.login),
            "broker": BROKER_NAME,
            "currency": ACCOUNT_CURRENCY,
            "balance": float(account.balance),
            "equity": float(account.equity),
            "margin": float(account.margin),
            "free_margin": float(account.margin_free),
            "margin_level": float(account.margin_level) if account.margin_level else 0,
            "profit": float(account.profit),
            "synced_at": datetime.now().isoformat(),
        }

    @staticmethod
    def sync():
        account = MT5Connector.account_info()

        if account is None:
            raise Exception("No MT5 account info available")

        payload = AccountSync.build_payload(account)

        SupabaseSync.upsert(
            "account_snapshots",
            payload,
            conflict_column="account_number"
        )

        return payload
