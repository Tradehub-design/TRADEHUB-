import os
import time

from automation.screenshot_importer import ScreenshotImporter


class ScreenshotWatcher:

    @staticmethod
    def scan_folder(folder_path):
        if not os.path.exists(folder_path):
            return []

        results = []

        for file_name in os.listdir(folder_path):
            local_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(local_path):
                continue

            if not ScreenshotImporter.is_supported(file_name):
                continue

            result = ScreenshotImporter.import_file(local_path)
            results.append(result)

        return results

    @staticmethod
    def watch(folder_path, interval_seconds=30):
        while True:
            ScreenshotWatcher.scan_folder(folder_path)
            time.sleep(interval_seconds)
