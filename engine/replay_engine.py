import pandas as pd


class ReplayEngine:

    @staticmethod
    def build_timeline(trade, screenshots=None):

        timeline = []

        timeline.append({
            "Stage": "Trade Open",
            "Time": trade.get("open_time"),
            "Status": "Completed"
        })

        if screenshots is not None and not screenshots.empty:

            shots = screenshots[
                screenshots["trade_id"] == trade.get("trade_id")
            ]

            for _, shot in shots.iterrows():

                timeline.append({

                    "Stage": shot.get("stage", "Screenshot"),

                    "Time": shot.get("created_at"),

                    "Status": "Available"

                })

        timeline.append({

            "Stage": "Trade Closed",

            "Time": trade.get("trade_date"),

            "Status": "Completed"

        })

        return pd.DataFrame(timeline)
