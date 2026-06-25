import pandas as pd


class CandleLoader:

    @staticmethod
    def clean_columns(df):
        df.columns = [
            str(col).strip().lower().replace(" ", "_")
            for col in df.columns
        ]
        return df

    @staticmethod
    def detect_columns(df):
        columns = {
            "time": None,
            "open": None,
            "high": None,
            "low": None,
            "close": None,
            "volume": None,
        }

        for column in df.columns:
            c = str(column).lower()

            if c in ["time", "date", "datetime", "candle_time"]:
                columns["time"] = column
            elif c in ["open", "open_price"]:
                columns["open"] = column
            elif c in ["high", "high_price"]:
                columns["high"] = column
            elif c in ["low", "low_price"]:
                columns["low"] = column
            elif c in ["close", "close_price"]:
                columns["close"] = column
            elif c in ["volume", "tick_volume", "vol"]:
                columns["volume"] = column

        return columns

    @staticmethod
    def load_csv(file):
        df = pd.read_csv(file)
        df = CandleLoader.clean_columns(df)
        return df
