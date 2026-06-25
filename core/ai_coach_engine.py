class AICoachEngine:

    @staticmethod
    def basic_stats(df):
        if df.empty:
            return {
                "total_trades": 0,
                "net_profit": 0,
                "win_rate": 0,
                "average_win": 0,
                "average_loss": 0,
            }

        wins = df[df["net_profit"] > 0]
        losses = df[df["net_profit"] < 0]

        return {
            "total_trades": len(df),
            "net_profit": round(df["net_profit"].sum(), 2),
            "win_rate": round((len(wins) / len(df)) * 100, 2),
            "average_win": round(wins["net_profit"].mean(), 2) if not wins.empty else 0,
            "average_loss": round(losses["net_profit"].mean(), 2) if not losses.empty else 0,
        }

    @staticmethod
    def best_worst_symbol(df):
        if df.empty or "symbol" not in df.columns:
            return "-", "-"

        result = df.groupby("symbol")["net_profit"].sum().sort_values()
        return result.index[-1], result.index[0]

    @staticmethod
    def best_worst_session(df):
        if df.empty or "session" not in df.columns:
            return "-", "-"

        result = df.groupby("session")["net_profit"].sum().sort_values()
        return result.index[-1], result.index[0]

    @staticmethod
    def discipline_score(reviews):
        if reviews.empty or "rule_score" not in reviews.columns:
            return 0
        return round(reviews["rule_score"].mean(), 2)

    @staticmethod
    def most_common_mistake(reviews):
        if reviews.empty or "mistake_type" not in reviews.columns:
            return "No mistake data yet"

        mistakes = reviews[reviews["mistake_type"] != "None"]

        if mistakes.empty:
            return "No repeated mistakes found"

        return mistakes["mistake_type"].value_counts().idxmax()

    @staticmethod
    def suggested_focus(win_rate, discipline, mistake):
        if discipline and discipline < 70:
            return "Improve rule discipline. Your checklist score is currently the biggest area to improve."

        if mistake not in ["No mistake data yet", "No repeated mistakes found"]:
            return f"Focus on reducing this repeated mistake: {mistake}."

        if win_rate < 45:
            return "Reduce trade frequency and only take your cleanest setups."

        return "Continue journaling every trade and start comparing performance by playbook."

    @staticmethod
    def generate_summary(df, reviews):
        stats = AICoachEngine.basic_stats(df)
        best_symbol, worst_symbol = AICoachEngine.best_worst_symbol(df)
        best_session, worst_session = AICoachEngine.best_worst_session(df)
        discipline = AICoachEngine.discipline_score(reviews)
        mistake = AICoachEngine.most_common_mistake(reviews)
        win_rate = stats["win_rate"]

        if win_rate >= 60:
            main_message = "Your win rate is strong. Focus on maximising winners and avoiding overtrading."
        elif win_rate >= 45:
            main_message = "Your win rate is moderate. Focus on filtering lower-quality setups."
        else:
            main_message = "Your win rate needs improvement. Focus on A-grade setups only."

        return {
            "main_message": main_message,
            "best_symbol": best_symbol,
            "worst_symbol": worst_symbol,
            "best_session": best_session,
            "worst_session": worst_session,
            "discipline_score": discipline,
            "most_common_mistake": mistake,
            "suggested_focus": AICoachEngine.suggested_focus(win_rate, discipline, mistake),
        }
