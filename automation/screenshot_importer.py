import os
from datetime import datetime

from utils.supabase_client import get_supabase_client
from data.data_engine import DataEngine
from core.screenshot_engine import ScreenshotEngine
from automation.screenshot_matcher import ScreenshotMatcher


class ScreenshotImporter:

    SUPPORTED = [".png", ".jpg", ".jpeg"]

    @staticmethod
    def is_supported(file_name):
        return os.path.splitext(file_name.lower())[1] in ScreenshotImporter.SUPPORTED

    @staticmethod
    def import_file(local_path):
        if not os.path.exists(local_path):
            return {
                "success": False,
                "message": "File does not exist",
            }

        file_name = os.path.basename(local_path)

        if not ScreenshotImporter.is_supported(file_name):
            return {
                "success": False,
                "message": "Unsupported file type",
            }

        supabase = get_supabase_client()
        trades = DataEngine.load_trades()

        matched_trade = ScreenshotMatcher.match_trade(
            file_name,
            trades
        )

        if not matched_trade:
            ScreenshotImporter.log_queue(
                file_name=file_name,
                file_path=local_path,
                status="unmatched",
                error_message="No matching trade found",
            )

            return {
                "success": False,
                "message": "No matching trade found",
            }

        ticket = matched_trade.get("ticket")
        account_number = matched_trade.get("account_number")
        screenshot_type = ScreenshotMatcher.detect_type(file_name)

        storage_path = ScreenshotEngine.build_file_path(
            ticket,
            account_number,
            screenshot_type,
            file_name
        )

        with open(local_path, "rb") as f:
            file_bytes = f.read()

        supabase.storage.from_("trade-screenshots").upload(
            storage_path,
            file_bytes,
            {
                "content-type": "image/jpeg",
                "upsert": "true",
            }
        )

        public_url = supabase.storage.from_("trade-screenshots").get_public_url(
            storage_path
        )

        payload = ScreenshotEngine.create_payload(
            ticket,
            account_number,
            screenshot_type,
            storage_path,
            public_url,
            f"Auto imported from {file_name}"
        )

        supabase.table("trade_screenshots").insert(payload).execute()

        ScreenshotImporter.log_queue(
            file_name=file_name,
            file_path=local_path,
            symbol=matched_trade.get("symbol"),
            screenshot_type=screenshot_type,
            trade_ticket=ticket,
            account_number=account_number,
            status="processed",
        )

        return {
            "success": True,
            "message": "Screenshot imported",
            "ticket": ticket,
            "type": screenshot_type,
        }

    @staticmethod
    def log_queue(
        file_name,
        file_path,
        symbol=None,
        screenshot_type=None,
        trade_ticket=None,
        account_number=None,
        status="pending",
        error_message=None,
    ):
        supabase = get_supabase_client()

        payload = {
            "file_name": file_name,
            "file_path": file_path,
            "symbol": symbol,
            "screenshot_type": screenshot_type,
            "trade_ticket": trade_ticket,
            "account_number": account_number,
            "status": status,
            "error_message": error_message,
            "processed_at": datetime.now().isoformat() if status == "processed" else None,
        }

        supabase.table("screenshot_import_queue").insert(payload).execute()
