import pandas as pd


class CandlePatterns:

    @staticmethod
    def liquidity_sweeps(df):
        df = df.copy()

        df["previous_high"] = df["high_price"].shift(1)
        df["previous_low"] = df["low_price"].shift(1)

        df["bullish_sweep"] = (
            (df["low_price"] < df["previous_low"]) &
            (df["close_price"] > df["previous_low"])
        )

        df["bearish_sweep"] = (
            (df["high_price"] > df["previous_high"]) &
            (df["close_price"] < df["previous_high"])
        )

        return df

    @staticmethod
    def continuation(df, body_percent=0.6):
        df = df.copy()

        candle_range = df["high_price"] - df["low_price"]
        body = abs(df["close_price"] - df["open_price"])

        df["body_percent"] = body / candle_range.replace(0, pd.NA)

        df["bullish"] = (
            (df["close_price"] > df["open_price"]) &
            (df["body_percent"] >= body_percent)
        )

        df["bearish"] = (
            (df["close_price"] < df["open_price"]) &
            (df["body_percent"] >= body_percent)
        )

        return df
