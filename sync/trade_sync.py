from datetime import datetime, timedelta

from sync.mt5_connector import MT5Connector
from sync.supabase_sync import SupabaseSync


class TradeSync:

    @staticmethod
    def build_payload(deal):
        direction = "BUY" if deal.type == 0 else "SELL"

        return {
            "ticket": int(deal.ticket),
            "account_number": str(deal.order),
            "symbol": deal.symbol,
            "direction": direction,
            "volume": float(deal.volume),
            "entry_price": float(deal.price),
            "exit_price": float(deal.price),
            "net_profit": float(deal.profit),
            "commission": float(deal.commission),
            "swap": float(deal.swap),
            "trade_date": datetime.fromtimestamp(deal.time).isoformat(),
            "session": "Unknown",
            "source": "MT5 Sync",
        }

    @staticmethod
    def sync(days_back=30):
        date_to = datetime.now()
        date_from = date_to - timedelta(days=days_back)

        deals = MT5Connector.history_deals(date_from, date_to)

        payloads = []

        for deal in deals:
            if not getattr(deal, "symbol", None):
                continue

            if float(deal.profit) == 0:
                continue

            payloads.append(
                TradeSync.build_payload(deal)
            )

        if payloads:
            SupabaseSync.upsert(
                "trades",
                payloads,
                conflict_column="ticket"
            )

        return payloads
