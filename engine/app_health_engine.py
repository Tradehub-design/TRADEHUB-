class AppHealthEngine:

    @staticmethod
    def check_tables(
        trades,
        reviews,
        screenshots,
        replays,
        account_snapshot=None,
        open_positions=None,
        sync_status=None,
    ):
        return {
            "trades_loaded": trades is not None and not trades.empty,
            "reviews_loaded": reviews is not None,
            "screenshots_loaded": screenshots is not None,
            "replays_loaded": replays is not None,
            "account_loaded": account_snapshot is not None and not account_snapshot.empty,
            "positions_loaded": open_positions is not None,
            "sync_loaded": sync_status is not None and not sync_status.empty,
            "trade_count": len(trades) if trades is not None else 0,
            "review_count": len(reviews) if reviews is not None else 0,
            "screenshot_count": len(screenshots) if screenshots is not None else 0,
            "replay_count": len(replays) if replays is not None else 0,
            "account_count": len(account_snapshot) if account_snapshot is not None else 0,
            "position_count": len(open_positions) if open_positions is not None else 0,
            "sync_count": len(sync_status) if sync_status is not None else 0,
        }

    @staticmethod
    def status_label(value):
        return "Connected" if value else "Waiting"

    @staticmethod
    def status_colour(value):
        return "positive" if value else "warning"
