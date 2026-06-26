import os
import time
import shutil

from automation.tradingview_importer import TradingViewImporter


class TradingViewWatcher:

    @staticmethod
    def ensure_folder(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    @staticmethod
    def archive_file(local_path, archive_folder):
        TradingViewWatcher.ensure_folder(archive_folder)

        file_name = os.path.basename(local_path)
        destination = os.path.join(archive_folder, file_name)

        if os.path.exists(destination):
            base, ext = os.path.splitext(file_name)
            destination = os.path.join(
                archive_folder,
                f"{base}_duplicate{ext}"
            )

        shutil.move(local_path, destination)

        return destination

    @staticmethod
    def scan_folder(folder_path, archive_folder=None):
        TradingViewWatcher.ensure_folder(folder_path)

        results = []

        for file_name in os.listdir(folder_path):
            local_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(local_path):
                continue

            if not TradingViewImporter.is_supported(file_name):
                continue

            result = TradingViewImporter.import_file(local_path)
            results.append(result)

            if result.get("success") and archive_folder:
                TradingViewWatcher.archive_file(
                    local_path,
                    archive_folder
                )

        return results

    @staticmethod
    def watch(folder_path, archive_folder=None, interval_seconds=30):
        TradingViewWatcher.ensure_folder(folder_path)

        while True:
            TradingViewWatcher.scan_folder(
                folder_path,
                archive_folder
            )

            time.sleep(interval_seconds)
