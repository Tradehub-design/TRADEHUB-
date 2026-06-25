import pandas as pd


class ResearchFilters:

    @staticmethod
    def filter_trades(
        df,
        symbol=None,
        session=None,
        direction=None,
        result=None,
        min_confidence=None,
        max_confidence=None,
        mistake_type=None,
        start_date=None,
        end_date=None,
    ):
        if df.empty:
            return df

        filtered = df.copy()

        if symbol and symbol != "All" and "symbol" in filtered.columns:
            filtered = filtered[filtered["symbol"] == symbol]

        if session and session != "All" and "session" in filtered.columns:
            filtered = filtered[filtered["session"] == session]

        if direction and direction != "All" and "direction" in filtered.columns:
            filtered = filtered[filtered["direction"] == direction]

        if result and result != "All" and "net_profit" in filtered.columns:
            if result == "Win":
                filtered = filtered[filtered["net_profit"] > 0]
            elif result == "Loss":
                filtered = filtered[filtered["net_profit"] < 0]
            elif result == "Breakeven":
                filtered = filtered[filtered["net_profit"] == 0]

        if start_date and "trade_date" in filtered.columns:
            filtered = filtered[filtered["trade_date"] >= pd.to_datetime(start_date)]

        if end_date and "trade_date" in filtered.columns:
            filtered = filtered[filtered["trade_date"] <= pd.to_datetime(end_date)]

        if "confidence_score" in filtered.columns:
            if min_confidence is not None:
                filtered = filtered[filtered["confidence_score"] >= min_confidence]
            if max_confidence is not None:
                filtered = filtered[filtered["confidence_score"] <= max_confidence]

        if mistake_type and mistake_type != "All" and "mistake_type" in filtered.columns:
            filtered = filtered[filtered["mistake_type"] == mistake_type]

        return filtered
