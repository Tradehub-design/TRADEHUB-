import os

from automation.tradingview_watcher import TradingViewWatcher


if __name__ == "__main__":
    folder = os.getenv(
        "TRADEHUB_TRADINGVIEW_FOLDER",
        "tradingview_screenshots"
    )

    archive_folder = os.getenv(
        "TRADEHUB_TRADINGVIEW_ARCHIVE",
        "tradingview_screenshots_archive"
    )

    interval = int(
        os.getenv(
            "TRADEHUB_TRADINGVIEW_INTERVAL",
            "30"
        )
    )

    TradingViewWatcher.watch(
        folder_path=folder,
        archive_folder=archive_folder,
        interval_seconds=interval
    )
