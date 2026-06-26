from data.data_engine import DataEngine


class DashboardEngine:

    @staticmethod
    def load():

        trades = DataEngine.load_trades()

        reviews = DataEngine.load_reviews()

        screenshots = DataEngine.load_screenshots()

        planner = DataEngine.load_daily_plan()

        return {
            "trades": trades,
            "reviews": reviews,
            "screenshots": screenshots,
            "planner": planner,
        }
