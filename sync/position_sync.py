from datetime import datetime

from sync.mt5_connector import MT5Connector
from sync.supabase_sync import SupabaseSync


class PositionSync:

    @staticmethod
    def build_payload(position):
        return {
            "ticket": int(position.ticket),
            "account_number": str(position.identifier),
            "symbol": position.symbol,
            "direction": "BUY" if position.type == 0 else "SELL",
            "volume": float(position.volume),
            "open_price": float(position.price_open),
            "current_price": float(position.price_current),
            "stop_loss": float(position.sl),
            "take_profit": float(position.tp),
            "profit": float(position.profit),
            "swap": float(position.swap),
            "opened_at": datetime.fromtimestamp(position.time).isoformat(),
            "synced_at": datetime.now().isoformat(),
        }

    @staticmethod
    def sync():
        positions = MT5Connector.open_positions()

        payloads = [
            PositionSync.build_payload(position)
            for position in positions
        ]

        if payloads:
            SupabaseSync.upsert(
                "open_positions",
                payloads,
                conflict_column="ticket"
            )

        return payloads
