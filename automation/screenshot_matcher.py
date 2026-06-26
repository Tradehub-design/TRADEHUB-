import re


class ScreenshotMatcher:

    SCREENSHOT_TYPES = [
        "before",
        "entry",
        "management",
        "exit",
        "review",
        "htf",
        "ltf",
        "mistake",
    ]

    @staticmethod
    def detect_symbol(file_name):
        upper_name = file_name.upper()

        symbols = [
            "EURUSD",
            "GBPUSD",
            "USDJPY",
            "USDCAD",
            "AUDUSD",
            "NZDUSD",
            "XAUUSD",
            "GBPJPY",
            "EURJPY",
            "GBPNZD",
            "CADJPY",
        ]

        for symbol in symbols:
            if symbol in upper_name:
                return symbol

        return None

    @staticmethod
    def detect_type(file_name):
        lower_name = file_name.lower()

        if "before" in lower_name:
            return "Before Entry"

        if "entry" in lower_name:
            return "Entry"

        if "manage" in lower_name:
            return "Trade Management"

        if "exit" in lower_name:
            return "Exit"

        if "review" in lower_name:
            return "Review"

        if "htf" in lower_name or "higher" in lower_name:
            return "Higher Timeframe"

        if "ltf" in lower_name or "lower" in lower_name:
            return "Lower Timeframe"

        if "mistake" in lower_name:
            return "Mistake"

        return "Other"

    @staticmethod
    def detect_ticket(file_name):
        match = re.search(r"\b\d{6,}\b", file_name)

        if match:
            return int(match.group())

        return None

    @staticmethod
    def match_trade(file_name, trades):
        ticket = ScreenshotMatcher.detect_ticket(file_name)

        if ticket and trades is not None and not trades.empty:
            matched = trades[trades["ticket"] == ticket]

            if not matched.empty:
                return matched.iloc[0].to_dict()

        symbol = ScreenshotMatcher.detect_symbol(file_name)

        if symbol and trades is not None and not trades.empty and "symbol" in trades.columns:
            matched = trades[trades["symbol"] == symbol]

            if not matched.empty:
                return matched.iloc[0].to_dict()

        return None
