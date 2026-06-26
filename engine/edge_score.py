class EdgeScoreEngine:

    @staticmethod
    def calculate(review, trade):
        score = 0

        if review is None:
            review = {}

        if trade is None:
            trade = {}

        if review.get("playbook_id"):
            score += 15

        rule_score = review.get("rule_score", 0) or 0
        score += min(float(rule_score) * 0.25, 25)

        confidence = review.get("confidence_score", 0) or 0
        score += min(float(confidence) * 1.5, 15)

        before = review.get("emotion_before")

        if before in ["Calm", "Confident"]:
            score += 15
        elif before == "Neutral":
            score += 8

        mistake = review.get("mistake_type")

        if mistake in ["None", None, ""]:
            score += 15

        pnl = trade.get("net_profit", 0) or 0

        try:
            pnl = float(pnl)
        except Exception:
            pnl = 0

        if pnl > 0:
            score += 15
        elif pnl == 0:
            score += 8

        score += 10

        return round(min(score, 100))
