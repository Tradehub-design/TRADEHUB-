class CoachEngine:

    @staticmethod
    def advice(report):

        advice = []

        if report["win_rate"] < 50:

            advice.append(
                "Reduce trading frequency and focus on A+ setups."
            )

        if report["best_symbol"] != report["worst_symbol"]:

            advice.append(
                f"Focus more on {report['best_symbol']}."
            )

            advice.append(
                f"Review why {report['worst_symbol']} performs poorly."
            )

        return advice
