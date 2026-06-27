import pandas as pd


class TradeMatchingEngine:

    @staticmethod
    def by_ticket(trades, ticket):
        if trades is None or trades.empty:
            return None

        if "ticket" not in trades.columns:
            return None

        matched = trades[
            trades["ticket"].astype(str) == str(ticket)
        ]

        if matched.empty:
            return None

        return matched.iloc[0].to_dict()

    @staticmethod
    def by_symbol_nearest_time(trades, symbol, target_time):
        if trades is None or trades.empty:
            return None

        if "symbol" not in trades.columns or "trade_date" not in trades.columns:
            return None

        df = trades.copy()

        df = df[
            df["symbol"].astype(str).str.upper() == str(symbol).upper()
        ]

        if df.empty:
            return None

        df["trade_date_dt"] = pd.to_datetime(
            df["trade_date"],
            errors="coerce"
        )

        target = pd.to_datetime(
            target_time,
            errors="coerce"
        )

        if pd.isna(target):
            return df.iloc[0].to_dict()

        df["distance"] = (
            df["trade_date_dt"] - target
        ).abs()

        df = df.sort_values("distance")

        return df.iloc[0].to_dict()

    @staticmethod
    def best_match(trades, ticket=None, symbol=None, target_time=None):
        if ticket:
            matched = TradeMatchingEngine.by_ticket(
                trades,
                ticket
            )

            if matched:
                return matched

        if symbol:
            return TradeMatchingEngine.by_symbol_nearest_time(
                trades,
                symbol,
                target_time
            )

        return None
