from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:

    APP_NAME = "TradeHub"

    VERSION = "0.5.4"

    AUTHOR = "TradeHub"

    CACHE_TTL = 60

    DEFAULT_MAX_RISK = 2.0

    DEFAULT_MAX_TRADES = 3

    DEFAULT_STOP_AFTER_LOSSES = 2

    DEFAULT_ACCOUNT = "Fusion Markets"

    DEFAULT_CURRENCY = "AUD"

    DEFAULT_THEME = "Dark"

    SCREENSHOT_BUCKET = "trade-screenshots"

    EDGE_PASS_SCORE = 80

    HIGH_CONFIDENCE = 8

    LOW_CONFIDENCE = 4
