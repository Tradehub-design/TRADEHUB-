class ScreenshotLinkEngine:

    @staticmethod
    def screenshots_for_trade(screenshots, ticket, account_number=None):
        if screenshots is None or screenshots.empty:
            return screenshots

        result = screenshots.copy()

        if "trade_ticket" in result.columns:
            result = result[result["trade_ticket"].astype(str) == str(ticket)]

        if account_number is not None and "account_number" in result.columns:
            result = result[result["account_number"].astype(str) == str(account_number)]

        return result

    @staticmethod
    def count_by_type(screenshots):
        if screenshots is None or screenshots.empty:
            return {}

        if "screenshot_type" not in screenshots.columns:
            return {}

        return screenshots["screenshot_type"].value_counts().to_dict()

    @staticmethod
    def timeline_order():
        return [
            "Higher Timeframe",
            "Lower Timeframe",
            "Before Entry",
            "Entry",
            "Trade Management",
            "Exit",
            "After Trade",
            "Review",
            "Mistake",
            "Other",
            "TradingView",
        ]
