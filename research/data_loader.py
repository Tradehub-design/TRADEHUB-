import pandas as pd


def clean_columns(df):
    df.columns = [
        str(c).strip().lower().replace(" ", "_")
        for c in df.columns
    ]
    return df


def find_column(df, options):
    for option in options:
        if option in df.columns:
            return option
    return None


def load_candle_csv(uploaded_file, symbol, timeframe):
    raw_df = pd.read_csv(uploaded_file)
    raw_df = clean_columns(raw_df)

    time_col = find_column(raw_df, ["time", "date", "datetime", "candle_time"])
    open_col = find_column(raw_df, ["open", "open_price"])
    high_col = find_column(raw_df, ["high", "high_price"])
    low_col = find_column(raw_df, ["low", "low_price"])
    close_col = find_column(raw_df, ["close", "close_price"])
    volume_col = find_column(raw_df, ["volume", "tick_volume", "vol"])

    required = [time_col, open_col, high_col, low_col, close_col]

    if any(col is None for col in required):
        return pd.DataFrame(), list(raw_df.columns)

    df = pd.DataFrame({
        "symbol": symbol,
        "timeframe": timeframe,
        "candle_time": pd.to_datetime(raw_df[time_col]),
        "open_price": pd.to_numeric(raw_df[open_col], errors="coerce"),
        "high_price": pd.to_numeric(raw_df[high_col], errors="coerce"),
        "low_price": pd.to_numeric(raw_df[low_col], errors="coerce"),
        "close_price": pd.to_numeric(raw_df[close_col], errors="coerce"),
        "volume": pd.to_numeric(raw_df[volume_col], errors="coerce") if volume_col else 0,
    })

    df = df.dropna(
        subset=[
            "candle_time",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
        ]
    )

    return df, list(raw_df.columns)
