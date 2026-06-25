class PatternEngine:

    @staticmethod
    def get_available_patterns():
        return [
            "Liquidity Sweep",
            "Continuation Candle",
        ]

    @staticmethod
    def run_pattern(df, pattern_name, settings, CandlePatterns):
        if pattern_name == "Liquidity Sweep":
            return CandlePatterns.liquidity_sweeps(df)

        if pattern_name == "Continuation Candle":
            body_threshold = settings.get("body_threshold", 0.6)
            return CandlePatterns.continuation(df, body_threshold)

        return df
