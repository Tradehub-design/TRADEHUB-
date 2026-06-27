import time
from datetime import datetime

from desktop_sync.config import DesktopSyncConfig
from desktop_sync.logger import DesktopLogger
from desktop_sync.mt5_client import MT5Client
from desktop_sync.supabase_client import DesktopSupabaseClient


class DesktopSyncAgent:

    @staticmethod
    def account_payload(account):
        return {
            "account_number": str(account.login),
            "broker": DesktopSyncConfig.BROKER_NAME,
            "currency": DesktopSyncConfig.ACCOUNT_CURRENCY,
            "balance": float(account.balance),
            "equity": float(account.equity),
            "margin": float(account.margin),
            "free_margin": float(account.margin_free),
            "margin_level": float(account.margin_level) if account.margin_level else 0,
            "profit": float(account.profit),
            "synced_at": datetime.now().isoformat(),
        }

    @staticmethod
    def position_payload(position, account_number):
        return {
            "ticket": int(position.ticket),
            "account_number": str(account_number),
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
    def trade_payload(deal, account_number):
        return {
            "ticket": int(deal.ticket),
            "account_number": str(account_number),
            "symbol": deal.symbol,
            "direction": "BUY" if deal.type == 0 else "SELL",
            "volume": float(deal.volume),
            "entry_price": float(deal.price),
            "exit_price": float(deal.price),
            "net_profit": float(deal.profit),
            "commission": float(deal.commission),
            "swap": float(deal.swap),
            "trade_date": datetime.fromtimestamp(deal.time).isoformat(),
            "session": "Unknown",
            "source": "Desktop MT5 Sync",
        }

    @staticmethod
    def sync_once():
        try:
            DesktopSupabaseClient.upsert(
                "sync_status",
                {
                    "id": 1,
                    "status": "running",
                    "message": "Desktop sync started",
                    "last_sync": datetime.now().isoformat(),
                },
                conflict_column="id"
            )

            MT5Client.connect()

            account = MT5Client.account_info()

            if account is None:
                raise Exception("MT5 account info unavailable")

            account_number = str(account.login)

            DesktopSupabaseClient.upsert(
                "account_snapshots",
                DesktopSyncAgent.account_payload(account),
                conflict_column="account_number"
            )

            positions = [
                DesktopSyncAgent.position_payload(position, account_number)
                for position in MT5Client.open_positions()
            ]

            if positions:
                DesktopSupabaseClient.upsert(
                    "open_positions",
                    positions,
                    conflict_column="ticket"
                )

            trades = []

            for deal in MT5Client.history_deals():
                if not getattr(deal, "symbol", None):
                    continue

                if float(deal.profit) == 0:
                    continue

                trades.append(
                    DesktopSyncAgent.trade_payload(
                        deal,
                        account_number
                    )
                )

            if trades:
                DesktopSupabaseClient.upsert(
                    "trades",
                    trades,
                    conflict_column="ticket"
                )

            DesktopSupabaseClient.upsert(
                "sync_status",
                {
                    "id": 1,
                    "status": "connected",
                    "message": f"Synced {len(trades)} trades and {len(positions)} open positions",
                    "last_sync": datetime.now().isoformat(),
                },
                conflict_column="id"
            )

            DesktopLogger.info(
                f"Sync complete: {len(trades)} trades, {len(positions)} positions"
            )

        except Exception as error:
            DesktopLogger.exception(f"Sync failed: {error}")

            try:
                DesktopSupabaseClient.upsert(
                    "sync_status",
                    {
                        "id": 1,
                        "status": "error",
                        "message": str(error),
                        "last_sync": datetime.now().isoformat(),
                    },
                    conflict_column="id"
                )
            except Exception:
                pass

        finally:
            try:
                MT5Client.disconnect()
            except Exception:
                pass

    @staticmethod
    def run_forever():
        DesktopLogger.info("TradeHub Desktop Sync Agent started")

        while True:
            DesktopSyncAgent.sync_once()
            time.sleep(DesktopSyncConfig.SYNC_INTERVAL_SECONDS)


if __name__ == "__main__":
    DesktopSyncAgent.run_forever()
