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
            "name": name or "",
            "description": description or "",
            "market": market or "Other",
            "timeframe": timeframe or "",
            "ideal_session": ideal_session or "Any",
            "risk_percent": risk_percent or 0,
            "target_rr": target_rr or 0,
        }

    @staticmethod
    def create_rule_payload(
        playbook_id,
        rule_text,
        rule_type,
        is_required
    ):
        return {
            "playbook_id": playbook_id,
            "rule_text": rule_text or "",
            "rule_type":
