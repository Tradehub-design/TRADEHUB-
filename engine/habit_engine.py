class HabitEngine:

    @staticmethod
    def detect(trades, reviews):
        habits = []

        if trades is not None and not trades.empty:
            if "symbol" in trades.columns and "net_profit" in trades.columns:
                symbol_perf = trades.groupby("symbol")["net_profit"].sum().sort_values()

                if not symbol_perf.empty:
                    worst = symbol_perf.index[0]
                    habits.append(f"Your weakest symbol is {worst} based on net P/L.")

            if "session" in trades.columns and "net_profit" in trades.columns:
                session_perf = trades.groupby("session")["net_profit"].sum().sort_values()

                if not session_perf.empty:
                    worst_session = session_perf.index[0]
                    habits.append(f"Your weakest session is {worst_session}.")

        if reviews is not None and not reviews.empty:
            if "mistake_type" in reviews.columns:
                mistakes = reviews[
                    (reviews["mistake_type"].notna())
                    & (reviews["mistake_type"] != "None")
                ]

                if not mistakes.empty:
                    common = mistakes["mistake_type"].mode().iloc[0]
                    habits.append(f"Most repeated mistake: {common}.")

        if not habits:
            habits.append("Complete more reviews to detect stronger behaviour patterns.")

        return habits
