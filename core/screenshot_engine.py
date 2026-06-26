import time


class ScreenshotEngine:

    @staticmethod
    def build_file_path(trade_ticket, account_number, screenshot_type, filename):
        safe_filename = filename.replace(" ", "_")
        timestamp = int(time.time())

        return f"{account_number}/{trade_ticket}/{screenshot_type}_{timestamp}_{safe_filename}"

    @staticmethod
    def create_payload(
        trade_ticket,
        account_number,
        screenshot_type,
        file_path,
        public_url,
        notes
    ):
        return {
            "trade_ticket": trade_ticket,
            "account_number": account_number,
            "screenshot_type": screenshot_type,
            "file_path": file_path,
            "public_url": public_url,
            "notes": notes,
        }
