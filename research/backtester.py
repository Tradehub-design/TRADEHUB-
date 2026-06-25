import pandas as pd


class ResearchBacktester:

    @staticmethod
    def follow_through(df, signal, direction, candles=5):
        output = []

        for i in range(len(df) - candles):
            if not bool(df.iloc[i][signal]):
                continue

            close = df.iloc[i]["close_price"]
            future = df.iloc[i + 1:i + candles + 1]

            if direction == "bullish":
                follow = future["high_price"].max() - close
                adverse = close - future["low_price"].min()
            else:
                follow = close - future["low_price"].min()
                adverse = future["high_price"].max() - close

            output.append({
                "time": df.iloc[i]["candle_time"],
                "worked": follow > adverse,
                "follow": follow,
                "adverse": adverse,
            })

        return pd.DataFrame(output)
