import pandas as pd


class AdvancedMetricsEngine:

    @staticmethod
    def hold_time_minutes(trades):
        if trades is None or trades.empty:
            return trades

        if "open_time" not in trades.columns or "trade_date" not in trades.columns:
            return trades

        df = trades.copy()

        df["open_time_dt"] = pd.to_datetime(
            df["open_time"],
            errors="coerce"
        )

        df["close_time_dt"] = pd.to_datetime(
            df["trade_date"],
            errors="coerce"
        )

        df["hold_minutes"] = (
            df["close_time_dt"] - df["open_time_dt"]
        ).dt.total_seconds() / 60

        return df

    @staticmethod
    def summary(trades):
        if trades is None or trades.empty or "net_profit" not in trades.columns:
            return {
                "average_hold_minutes": 0,
                "best_trade": 0,
                "worst_trade": 0,
                "largest_symbol": "-",
                "most_traded_symbol": "-",
                "best_day": "-",
                "worst_day": "-",
            }

        df = AdvancedMetricsEngine.hold_time_minutes(trades)

        average_hold = 0

        if "hold_minutes" in df.columns:
            average_hold = round(
                df["hold_minutes"].dropna().mean(),
                1
            ) if not df["hold_minutes"].dropna().empty else 0

        most_traded_symbol = "-"

        if "symbol" in df.columns:
            most_traded_symbol = df["symbol"].mode().iloc[0]

        largest_symbol = "-"

        if "symbol" in df.columns:
            symbol_net = df.groupby("symbol")["net_profit"].sum()

            if not symbol_net.empty:
                largest_symbol = symbol_net.sort_values(ascending=False).index[0]

        best_day = "-"
        worst_day = "-"

        if "trade_date" in df.columns:
            temp = df.copy()
            temp["day"] = pd.to_datetime(
                temp["trade_date"],
                errors="coerce"
            ).dt.date

            daily = temp.groupby("day")["net_profit"].sum()

            if not daily.empty:
                best_day = str(daily.sort_values(ascending=False).index[0])
                worst_day = str(daily.sort_values(ascending=True).index[0])

        return {
            "average_hold_minutes": average_hold,
            "best_trade": round(df["net_profit"].max(), 2),
            "worst_trade": round(df["net_profit"].min(), 2),
            "largest_symbol": largest_symbol,
            "most_traded_symbol": most_traded_symbol,
            "best_day": best_day,
            "worst_day": worst_day,
        }
