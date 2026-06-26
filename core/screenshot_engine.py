import time


class ScreenshotEngine:

    @staticmethod
    def clean_text(value):
        if value is None:
            return "unknown"

        value = str(value)
        value = value.replace(" ", "_")
        value = value.replace("/", "_")
        value = value.replace("\\", "_")
        value = value.replace(":", "_")
        value = value.replace("|", "_")

        return value

    @staticmethod
    def build_file_path(trade_ticket, account_number, screenshot_type, filename):
        safe_filename = ScreenshotEngine.clean_text(filename)
        safe_type = ScreenshotEngine.clean_text(screenshot_type)
        safe_account = ScreenshotEngine.clean_text(account_number)
        safe_ticket = ScreenshotEngine.clean_text(trade_ticket)
        timestamp = int(time.time())

        return f"{safe_account}/{safe_ticket}/{safe_type}_{timestamp}_{safe_filename}"

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
