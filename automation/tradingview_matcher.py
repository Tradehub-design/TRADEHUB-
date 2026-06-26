import re


class TradingViewMatcher:

    SYMBOLS = [
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
        "US30",
        "NAS100",
        "BTCUSD",
        "ETHUSD",
    ]

    TIMEFRAMES = [
        "1M",
        "3M",
        "5M",
        "15M",
        "30M",
        "1H",
        "4H",
        "1D",
        "1W",
    ]

    @staticmethod
    def detect_symbol(file_name):
        name = file_name.upper().replace("_", "").replace("-", "")

        for symbol in TradingViewMatcher.SYMBOLS:
            if symbol in name:
                return symbol

        return None

    @staticmethod
    def detect_timeframe(file_name):
        name = file_name.upper()

        for timeframe in TradingViewMatcher.TIMEFRAMES:
            pattern = rf"\b{timeframe}\b"

            if re.search(pattern, name):
                return timeframe

        if "HTF" in name or "HIGHER" in name:
            return "HTF"

        if "LTF" in name or "LOWER" in name:
            return "LTF"

        return "Unknown"

    @staticmethod
    def detect_type(file_name):
        name = file_name.lower()

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

        if "htf" in name or "higher" in name:
            return "Higher Timeframe"

        if "ltf" in name or "lower" in name:
            return "Lower Timeframe"

        if "mistake" in name:
            return "Mistake"

        return "TradingView"

    @staticmethod
    def detect_ticket(file_name):
        match = re.search(r"\b\d{6,}\b", file_name)

        if match:
            return int(match.group())

        return None

    @staticmethod
    def match_trade(file_name, trades):
        if trades is None or trades.empty:
            return None

        ticket = TradingViewMatcher.detect_ticket(file_name)

        if ticket and "ticket" in trades.columns:
            matched = trades[trades["ticket"] == ticket]

            if not matched.empty:
                return matched.iloc[0].to_dict()

        symbol = TradingViewMatcher.detect_symbol(file_name)

        if symbol and "symbol" in trades.columns:
            matched = trades[trades["symbol"] == symbol]

            if not matched.empty:
                return matched.iloc[0].to_dict()

        return None
