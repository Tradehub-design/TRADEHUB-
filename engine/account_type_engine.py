class AccountTypeEngine:

    @staticmethod
    def classify(account_number):
        value = str(account_number).lower()

        if "funded" in value:
            return "Funded"

        if "challenge" in value:
            return "Challenge"

        if "demo" in value:
            return "Demo"

        if "real_sample" in value:
            return "Demo Dataset"

        return "Live"

    @staticmethod
    def options():
        return ["All", "Live", "Funded", "Challenge", "Demo", "Demo Dataset"]
