import os
from datetime import datetime

from utils.supabase_client import get_supabase_client
from data.data_engine import DataEngine
from core.screenshot_engine import ScreenshotEngine
from automation.tradingview_matcher import TradingViewMatcher


class TradingViewImporter:

    SUPPORTED = [".png", ".jpg", ".jpeg"]

    @staticmethod
    def is_supported(file_name):
        return os.path.splitext(file_name.lower())[1] in TradingViewImporter.SUPPORTED

    @staticmethod
    def import_file(local_path):
        if not os.path.exists(local_path):
            return {
                "success": False,
                "message": "File does not exist",
            }

        file_name = os.path.basename(local_path)

        if not TradingViewImporter.is_supported(file_name):
            return {
                "success": False,
                "message": "Unsupported file type",
            }

        supabase = get_supabase_client()
        trades = DataEngine.load_trades()

        matched_trade = TradingViewMatcher.match_trade(
            file_name,
            trades
        )

        symbol = TradingViewMatcher.detect_symbol(file_name)
        timeframe = TradingViewMatcher.detect_timeframe(file_name)
        screenshot_type = TradingViewMatcher.detect_type(file_name)

        if not matched_trade:
            TradingViewImporter.log_queue(
                file_name=file_name,
                file_path=local_path,
                detected_symbol=symbol,
                detected_timeframe=timeframe,
                detected_screenshot_type=screenshot_type,
                status="unmatched",
                error_message="No matching trade found",
            )

            return {
                "success": False,
                "message": "No matching trade found",
                "symbol": symbol,
                "timeframe": timeframe,
            }

        ticket = matched_trade.get("ticket")
        account_number = matched_trade.get("account_number")

        storage_path = ScreenshotEngine.build_file_path(
            ticket,
            account_number,
            screenshot_type,
            file_name
        )

        with open(local_path, "rb") as file:
            file_bytes = file.read()

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
            f"Auto imported TradingView screenshot: {file_name}"
        )

        supabase.table("trade_screenshots").insert(payload).execute()

        TradingViewImporter.log_queue(
            file_name=file_name,
            file_path=local_path,
            detected_symbol=symbol,
            detected_timeframe=timeframe,
            detected_screenshot_type=screenshot_type,
            matched_trade_ticket=ticket,
            account_number=account_number,
            status="processed",
        )

        return {
            "success": True,
            "message": "TradingView screenshot imported",
            "ticket": ticket,
            "symbol": symbol,
            "timeframe": timeframe,
            "type": screenshot_type,
        }

    @staticmethod
    def log_queue(
        file_name,
        file_path,
        detected_symbol=None,
        detected_timeframe=None,
        detected_screenshot_type=None,
        matched_trade_ticket=None,
        account_number=None,
        status="pending",
        error_message=None,
    ):
        supabase = get_supabase_client()

        payload = {
            "file_name": file_name,
            "file_path": file_path,
            "detected_symbol": detected_symbol,
            "detected_timeframe": detected_timeframe,
            "detected_screenshot_type": detected_screenshot_type,
            "matched_trade_ticket": matched_trade_ticket,
            "account_number": account_number,
            "status": status,
            "error_message": error_message,
            "processed_at": datetime.now().isoformat() if status == "processed" else None,
        }

        supabase.table("tradingview_import_queue").insert(payload).execute()
