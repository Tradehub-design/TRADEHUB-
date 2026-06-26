from datetime import date


class PlannerEngine:

    @staticmethod
    def default_plan():

        return {
            "plan_date": str(date.today()),
            "market_bias": {},
            "focus": [],
            "news": [],
            "max_risk": 2,
            "max_trades": 3,
            "stop_after_losses": 2,
            "sleep": 4,
            "stress": 2,
            "confidence": 4,
            "goals": [],
            "notes": ""
        }

    @staticmethod
    def build_payload(
        plan_date,
        market_bias,
        focus,
        news,
        max_risk,
        max_trades,
        stop_after_losses,
        sleep,
        stress,
        confidence,
        goals,
        notes
    ):

        return {
            "plan_date": plan_date,
            "market_bias": market_bias,
            "focus": focus,
            "news": news,
            "max_risk": max_risk,
            "max_trades": max_trades,
            "stop_after_losses": stop_after_losses,
            "sleep": sleep,
            "stress": stress,
            "confidence": confidence,
            "goals": goals,
            "notes": notes
        }
