class ReviewIntelligenceEngine:

    @staticmethod
    def summary(reviews):
        if reviews is None or reviews.empty:
            return {
                "review_count": 0,
                "average_rule_score": 0,
                "average_confidence": 0,
                "most_common_mistake": "-",
            }

        avg_rule = 0
        avg_confidence = 0
        mistake = "-"

        if "rule_score" in reviews.columns:
            avg_rule = round(reviews["rule_score"].fillna(0).mean(), 1)

        if "confidence_score" in reviews.columns:
            avg_confidence = round(reviews["confidence_score"].fillna(0).mean(), 1)

        if "mistake_type" in reviews.columns:
            mistakes = reviews[
                (reviews["mistake_type"].notna())
                & (reviews["mistake_type"] != "None")
            ]

            if not mistakes.empty:
                mistake = mistakes["mistake_type"].mode().iloc[0]

        return {
            "review_count": len(reviews),
            "average_rule_score": avg_rule,
            "average_confidence": avg_confidence,
            "most_common_mistake": mistake,
        }
