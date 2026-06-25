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
