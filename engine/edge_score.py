class EdgeScoreEngine:

    @staticmethod
    def calculate(review, trade):

        score = 0

        # -------------------------
        # Playbook
        # -------------------------

        if review.get("playbook_id"):
            score += 15

        # -------------------------
        # Rule Score
        # -------------------------

        rule_score = review.get("rule_score", 0)

        score += min(rule_score * 0.25, 25)

        # -------------------------
        # Confidence
        # -------------------------

        confidence = review.get("confidence_score", 0)

        score += min(confidence * 1.5, 15)

        # -------------------------
        # Psychology
        # -------------------------

        before = review.get("emotion_before")

        if before in ["Calm", "Confident"]:
            score += 15

        elif before in ["Neutral"]:
            score += 8

        # -------------------------
        # Mistakes
        # -------------------------

        mistake = review.get("mistake_type")

        if mistake == "None":
            score += 15

        # -------------------------
        # Profit
        # -------------------------

        pnl = trade.get("net_profit", 0)

        if pnl > 0:
            score += 15

        elif pnl == 0:
            score += 8

        # -------------------------
        # Risk
        # -------------------------

        score += 10

        return round(score)
