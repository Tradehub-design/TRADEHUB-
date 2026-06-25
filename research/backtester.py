import pandas as pd


def analyse_follow_through(df, signal_col, direction, lookahead=5):
    results = []

    for i in range(len(df) - lookahead):
        if not df.iloc[i][signal_col]:
            continue

        entry_close = df.iloc[i]["close_price"]
        future = df.iloc[i + 1:i + 1 + lookahead]

        if direction == "bullish":
            max_follow = future["high_price"].max() - entry_close
            max_adverse = entry_close - future["low_price"].min()
        else:
            max_follow = entry_close - future["low_price"].min()
            max_adverse = future["high_price"].max() - entry_close

        results.append({
            "candle_time": df.iloc[i]["candle_time"],
            "entry_close": entry_close,
            "max_follow_through": max_follow,
            "max_adverse_move": max_adverse,
            "worked": max_follow > max_adverse,
        })

    return pd.DataFrame(results)
