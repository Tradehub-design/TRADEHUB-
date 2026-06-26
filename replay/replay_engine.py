class ReplayEngine:

    @staticmethod
    def build_payload(
        trade_ticket,
        account_number,
        summary,
        lessons,
        improvements
    ):
        return {
            "trade_ticket": trade_ticket,
            "account_number": account_number,
            "summary": summary or "",
            "lessons": lessons or "",
            "improvements": improvements or "",
        }
