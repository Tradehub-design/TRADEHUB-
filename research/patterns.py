import pandas as pd


def detect_liquidity_sweeps(df):
    df = df.copy()

    df["prev_high"] = df["high_price"].shift(1)
    df["prev_low"] = df["low_price"].shift(1)

    df["bullish_sweep"] = (
        (df["low_price"] < df["prev_low"]) &
        (df["close_price"] > df["prev_low"])
    )

    df["bearish_sweep"] = (
        (df["high_price"] > df["prev_high"]) &
        (df["close_price"] < df["prev_high"])
    )

    return df


def detect_continuation_candles(df, body_threshold=0.6):
    df = df.copy()

    candle_range = df["high_price"] - df["low_price"]
    body_size = abs(df["close_price"] - df["open_price"])

    df["body_percent"] = body_size / candle_range.replace(0, pd.NA)

    df["bullish_continuation"] = (
        (df["close_price"] > df["open_price"]) &
        (df["body_percent"] >= body_threshold)
    )

    df["bearish_continuation"] = (
        (df["close_price"] < df["open_price"]) &
        (df["body_percent"] >= body_threshold)
    )

    return df
