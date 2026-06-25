class JournalEngine:

    @staticmethod
    def calculate_rule_score(rules_followed, total_rules):
        if not total_rules:
            return 0

        return round((rules_followed / total_rules) * 100, 2)

    @staticmethod
    def grade_trade(rule_score, confidence_score, mistake_type):
        if mistake_type and mistake_type != "None":
            if rule_score >= 80:
                return "B"
            return "C"

        if rule_score >= 90 and confidence_score >= 8:
            return "A+"

        if rule_score >= 80:
            return "A"

        if rule_score >= 65:
            return "B"

        if rule_score >= 50:
            return "C"

        return "F"

    @staticmethod
    def create_review_payload(
        trade_ticket,
        account_number,
        playbook_id,
        rules_followed,
        total_rules,
        confidence_score,
        emotion_before,
        emotion_after,
        mistake_type,
        lesson_learned,
        journal_notes
    ):
        rule_score = JournalEngine.calculate_rule_score(
            rules_followed,
            total_rules
        )

        trade_grade = JournalEngine.grade_trade(
            rule_score,
            confidence_score,
            mistake_type
        )

        return {
            "trade_ticket": trade_ticket,
            "account_number": account_number,
            "playbook_id": playbook_id,
            "trade_grade": trade_grade,
            "confidence_score": confidence_score,
            "emotion_before": emotion_before,
            "emotion_after": emotion_after,
            "mistake_type": mistake_type,
            "rules_followed": rules_followed,
            "total_rules": total_rules,
            "rule_score": rule_score,
            "lesson_learned": lesson_learned,
            "journal_notes": journal_notes,
        }
