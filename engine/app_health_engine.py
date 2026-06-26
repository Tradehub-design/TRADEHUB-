class AppHealthEngine:

    @staticmethod
    def check_tables(trades, reviews, screenshots, replays):
        return {
            "trades_loaded": trades is not None and not trades.empty,
            "reviews_loaded": reviews is not None,
            "screenshots_loaded": screenshots is not None,
            "replays_loaded": replays is not None,
            "trade_count": len(trades) if trades is not None else 0,
            "review_count": len(reviews) if reviews is not None else 0,
            "screenshot_count": len(screenshots) if screenshots is not None else 0,
            "replay_count": len(replays) if replays is not None else 0,
        }

    @staticmethod
    def status_label(value):
        return "Connected" if value else "Waiting"

    @staticmethod
    def status_colour(value):
        return "positive" if value else "warning"
