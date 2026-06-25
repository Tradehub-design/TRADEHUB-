class PlaybookEngine:

    @staticmethod
    def create_playbook_payload(
        name,
        description,
        market,
        timeframe,
        ideal_session,
        risk_percent,
        target_rr
    ):
        return {
            "name": name,
            "description": description,
            "market": market,
            "timeframe": timeframe,
            "ideal_session": ideal_session,
            "risk_percent": risk_percent,
            "target_rr": target_rr,
            "is_active": True,
        }

    @staticmethod
    def create_rule_payload(playbook_id, rule_text, rule_type, is_required=True):
        return {
            "playbook_id": playbook_id,
            "rule_text": rule_text,
            "rule_type": rule_type,
            "is_required": is_required,
        }

    @staticmethod
    def calculate_rule_score(total_rules, rules_followed):
        if total_rules == 0:
            return 0

        return round((rules_followed / total_rules) * 100, 2)
