import logging
import os


LOG_DIR = "desktop_sync/logs"
LOG_FILE = os.path.join(LOG_DIR, "tradehub_desktop_sync.log")


os.makedirs(LOG_DIR, exist_ok=True)


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


logger = logging.getLogger("TradeHubDesktopSync")


class DesktopLogger:

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
