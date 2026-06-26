import logging
import os

LOG_DIR = "sync_logs"
LOG_FILE = os.path.join(LOG_DIR, "tradehub_sync.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("TradeHubSync")


class SyncLogger:

    @staticmethod
    def info(message):
        logger.info(message)
        print(message)

    @staticmethod
    def warning(message):
        logger.warning(message)
        print(message)

    @staticmethod
    def error(message):
        logger.error(message)
        print(message)

    @staticmethod
    def exception(message):
        logger.exception(message)
        print(message)
