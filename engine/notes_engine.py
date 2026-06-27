import pandas as pd


class NotesEngine:

    @staticmethod
    def empty():

        return pd.DataFrame(

            columns=[

                "trade_id",

                "title",

                "note",

                "created"

            ]

        )
