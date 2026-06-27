class LiveAccountHealthEngine:

    @staticmethod
    def calculate(account_snapshot, open_positions):
        if account_snapshot is None or account_snapshot.empty:
            return {
                "status": "Offline",
                "balance": 0,
                "equity": 0,
                "floating_pl": 0,
                "margin_level": 0,
                "open_positions": 0,
                "risk_status": "Waiting",
            }

        account = account_snapshot.iloc[0]

        balance = float(account.get("balance", 0) or 0)
        equity = float(account.get("equity", 0) or 0)
        floating_pl = float(account.get("profit", 0) or 0)
        margin_level = float(account.get("margin_level", 0) or 0)

        position_count = 0

        if open_positions is not None:
            position_count = len(open_positions)

        if margin_level == 0:
            risk_status = "No Margin Used"
        elif margin_level >= 500:
            risk_status = "Healthy"
        elif margin_level >= 200:
            risk_status = "Caution"
        else:
            risk_status = "Danger"

        return {
            "status": "Connected",
            "balance": round(balance, 2),
            "equity": round(equity, 2),
            "floating_pl": round(floating_pl, 2),
            "margin_level": round(margin_level, 2),
            "open_positions": position_count,
            "risk_status": risk_status,
        }
