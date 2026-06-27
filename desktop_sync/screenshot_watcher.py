import os
import shutil
import time
from datetime import datetime

from desktop_sync.logger import DesktopLogger
from desktop_sync.supabase_client import DesktopSupabaseClient


class DesktopScreenshotWatcher:

    SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg"]

    @staticmethod
    def is_supported(file_name):
        return os.path.splitext(file_name.lower())[1] in DesktopScreenshotWatcher.SUPPORTED_EXTENSIONS

    @staticmethod
    def clean(value):
        value = str(value or "unknown")
        value = value.replace(" ", "_")
        value = value.replace("/", "_")
        value = value.replace("\\", "_")
        value = value.replace(":", "_")
        return value

    @staticmethod
    def detect_type(file_name):
        name = file_name.lower()

        if "htf" in name or "higher" in name:
            return "Higher Timeframe"

        if "ltf" in name or "lower" in name:
            return "Lower Timeframe"

        if "before" in name:
            return "Before Entry"

        if "entry" in name:
            return "Entry"

        if "manage" in name:
            return "Trade Management"

        if "exit" in name:
            return "Exit"

        if "review" in name:
            return "Review"

        return "Other"

    @staticmethod
    def upload_file(local_path, account_number="desktop_sync", trade_ticket=None):
        file_name = os.path.basename(local_path)
        screenshot_type = DesktopScreenshotWatcher.detect_type(file_name)

        storage_path = (
            f"{DesktopScreenshotWatcher.clean(account_number)}/"
            f"{DesktopScreenshotWatcher.clean(trade_ticket or 'unmatched')}/"
            f"{DesktopScreenshotWatcher.clean(screenshot_type)}_"
            f"{int(time.time())}_"
            f"{DesktopScreenshotWatcher.clean(file_name)}"
        )

        with open(local_path, "rb") as file:
            file_bytes = file.read()

        client = DesktopSupabaseClient.client()

        client.storage.from_("trade-screenshots").upload(
            storage_path,
            file_bytes,
            {
                "content-type": "image/jpeg",
                "upsert": "true",
            }
        )

        public_url = client.storage.from_("trade-screenshots").get_public_url(
            storage_path
        )

        payload = {
            "trade_ticket": trade_ticket,
            "account_number": account_number,
            "screenshot_type": screenshot_type,
            "file_path": storage_path,
            "public_url": public_url,
            "notes": f"Desktop auto-upload: {file_name}",
            "created_at": datetime.now().isoformat(),
        }

        DesktopSupabaseClient.insert(
            "trade_screenshots",
            payload
        )

        return payload

    @staticmethod
    def scan_folder(folder_path, archive_folder=None):
        os.makedirs(folder_path, exist_ok=True)

        if archive_folder:
            os.makedirs(archive_folder, exist_ok=True)

        uploaded = []

        for file_name in os.listdir(folder_path):
            local_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(local_path):
                continue

            if not DesktopScreenshotWatcher.is_supported(file_name):
                continue

            try:
                payload = DesktopScreenshotWatcher.upload_file(local_path)
                uploaded.append(payload)

                if archive_folder:
                    shutil.move(
                        local_path,
                        os.path.join(archive_folder, file_name)
                    )

            except Exception as error:
                DesktopLogger.exception(
                    f"Screenshot upload failed for {file_name}: {error}"
                )

        return uploaded

    @staticmethod
    def watch(folder_path, archive_folder=None, interval_seconds=30):
        DesktopLogger.info(f"Watching screenshot folder: {folder_path}")

        while True:
            DesktopScreenshotWatcher.scan_folder(
                folder_path,
                archive_folder
            )

            time.sleep(interval_seconds)


if __name__ == "__main__":
    folder = os.getenv(
        "TRADEHUB_SCREENSHOT_FOLDER",
        "desktop_sync/screenshots"
    )

    archive = os.getenv(
        "TRADEHUB_SCREENSHOT_ARCHIVE",
        "desktop_sync/screenshots_archive"
    )

    DesktopScreenshotWatcher.watch(
        folder,
        archive
    )
