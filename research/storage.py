import pandas as pd


class CandleStorage:

    @staticmethod
    def save_candles(supabase, df):
        rows = df.to_dict("records")

        for row in rows:
            row["candle_time"] = row["candle_time"].isoformat()

        supabase.table("candle_data").upsert(
            rows,
            on_conflict="symbol,timeframe,candle_time"
        ).execute()

        return len(rows)

    @staticmethod
    def load_candles(supabase, symbol, timeframe):
        response = (
            supabase.table("candle_data")
            .select("*")
            .eq("symbol", symbol)
            .eq("timeframe", timeframe)
            .order("candle_time")
            .execute()
        )

        if not response.data:
            return pd.DataFrame()

        df = pd.DataFrame(response.data)

        df["candle_time"] = pd.to_datetime(df["candle_time"])
        df["open_price"] = pd.to_numeric(df["open_price"], errors="coerce")
        df["high_price"] = pd.to_numeric(df["high_price"], errors="coerce")
        df["low_price"] = pd.to_numeric(df["low_price"], errors="coerce")
        df["close_price"] = pd.to_numeric(df["close_price"], errors="coerce")

        return df
