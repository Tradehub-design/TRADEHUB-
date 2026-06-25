PATTERN_REGISTRY = {
    "Liquidity Sweep": {
        "description": "Detects candles that sweep the previous high or low and close back inside.",
        "bullish_signal": "bullish_sweep",
        "bearish_signal": "bearish_sweep",
    },
    "Continuation Candle": {
        "description": "Detects strong body candles that may continue in the same direction.",
        "bullish_signal": "bullish",
        "bearish_signal": "bearish",
    },
}
