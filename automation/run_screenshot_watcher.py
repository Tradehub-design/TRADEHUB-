import os

from automation.screenshot_watcher import ScreenshotWatcher


if __name__ == "__main__":
    folder = os.getenv(
        "TRADEHUB_SCREENSHOT_FOLDER",
        "screenshots_to_import"
    )

    interval = int(
        os.getenv(
            "TRADEHUB_SCREENSHOT_INTERVAL",
            "30"
        )
    )

    ScreenshotWatcher.watch(
        folder,
        interval
    )
