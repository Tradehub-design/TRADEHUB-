import time

from sync.config import SYNC_INTERVAL_SECONDS
from sync.run_sync import run_once
from sync.sync_logger import SyncLogger


def start():
    SyncLogger.info("TradeHub Sync Scheduler started")

    while True:
        run_once()
        SyncLogger.info(f"Sleeping for {SYNC_INTERVAL_SECONDS} seconds")
        time.sleep(SYNC_INTERVAL_SECONDS)


if __name__ == "__main__":
    start()
