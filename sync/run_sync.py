from sync.mt5_connector import MT5Connector
from sync.account_sync import AccountSync
from sync.position_sync import PositionSync
from sync.trade_sync import TradeSync
from sync.status_sync import StatusSync
from sync.sync_logger import SyncLogger


def run_once():
    try:
        StatusSync.update("running", "Sync started")

        MT5Connector.connect()

        account = AccountSync.sync()
        positions = PositionSync.sync()
        trades = TradeSync.sync(days_back=30)

        StatusSync.update(
            "connected",
            f"Synced {len(trades)} trades and {len(positions)} open positions"
        )

        SyncLogger.info("--------------------------------")
        SyncLogger.info("TradeHub Sync Complete")
        SyncLogger.info(f"Account: {account.get('account_number')}")
        SyncLogger.info(f"Open Positions: {len(positions)}")
        SyncLogger.info(f"Trades Synced: {len(trades)}")
        SyncLogger.info("--------------------------------")

    except Exception as e:
        StatusSync.update("error", str(e))
        SyncLogger.exception(f"Sync failed: {e}")

    finally:
        try:
            MT5Connector.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    run_once()
