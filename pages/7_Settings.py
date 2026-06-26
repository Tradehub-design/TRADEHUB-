import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row
from core.config import AppConfig
from engine.cache_engine import CacheEngine


load_css()

app_header(
    "⚙ Settings",
    "Application settings, cache controls and system information."
)

section("Application")

stat_row([
    {
        "label": "App",
        "value": AppConfig.APP_NAME,
        "helper": "Trading platform",
        "status": "neutral",
    },
    {
        "label": "Version",
        "value": AppConfig.VERSION,
        "helper": "Current build",
        "status": "positive",
    },
    {
        "label": "Theme",
        "value": AppConfig.DEFAULT_THEME,
        "helper": "Professional dark mode",
        "status": "neutral",
    },
])

section("Trading Defaults")

stat_row([
    {
        "label": "Default Account",
        "value": AppConfig.DEFAULT_ACCOUNT,
        "helper": "Primary broker",
        "status": "neutral",
    },
    {
        "label": "Currency",
        "value": AppConfig.DEFAULT_CURRENCY,
        "helper": "Reporting currency",
        "status": "neutral",
    },
    {
        "label": "Cache TTL",
        "value": f"{AppConfig.CACHE_TTL}s",
        "helper": "Data refresh window",
        "status": "neutral",
    },
])

section("Cache")

command_card(
    "Refresh Cached Data",
    "If the app does not immediately show updated data, clear the cache below.",
    "This does not delete any data."
)

if st.button("Clear App Cache"):
    CacheEngine.clear()
    st.success("Cache cleared. Refresh the page if needed.")

section("Version 1 Status")

command_card(
    "Current Focus",
    "TradeHub is in Version 1 polish mode. Existing pages are being redesigned and connected before MT5 Sync is completed on desktop.",
    "No data is changed from this page."
)
