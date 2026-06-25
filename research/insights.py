class ResearchInsights:

    @staticmethod
    def best_and_worst(df, column):
        if df.empty or column not in df.columns or "net_profit" not in df.columns:
            return "-", "-"

        grouped = df.groupby(column)["net_profit"].sum().sort_values()

        if grouped.empty:
            return "-", "-"

        return grouped.index[-1], grouped.index[0]

    @staticmethod
    def most_expensive_mistake(df):
        if df.empty or "mistake_type" not in df.columns or "net_profit" not in df.columns:
            return "-"

        mistakes = df[df["mistake_type"].notna()]
        mistakes = mistakes[mistakes["mistake_type"] != "None"]

        if mistakes.empty:
            return "-"

        grouped = mistakes.groupby("mistake_type")["net_profit"].sum().sort_values()

        return grouped.index[0]

    @staticmethod
    def confidence_bucket(value):
        if value >= 8:
            return "High 8-10"
        if value >= 5:
            return "Medium 5-7"
        return "Low 0-4"

    @staticmethod
    def add_confidence_bucket(df):
        if df.empty or "confidence_score" not in df.columns:
            return df

        temp = df.copy()
        temp["confidence_bucket"] = temp["confidence_score"].fillna(0).apply(
            ResearchInsights.confidence_bucket
        )

        return temp
