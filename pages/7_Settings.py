import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row
from core.config import AppConfig
from data.data_engine import DataEngine
from engine.cache_engine import CacheEngine
from engine.app_health_engine import AppHealthEngine


load_css()

app_header(
    "⚙ Settings",
    "Application settings, cache controls and system health."
)

trades = DataEngine.load_trades()
reviews = DataEngine.load_reviews()
screenshots = DataEngine.load_screenshots()
replays = DataEngine.load_replays()
sync_status = DataEngine.load_sync_status()

health = AppHealthEngine.check_tables(
    trades,
    reviews,
    screenshots,
    replays
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

section("Sync Status")

if sync_status.empty:
    stat_row([
        {
            "label": "MT5 Sync",
            "value": "Not Connected",
            "helper": "Run desktop sync agent",
            "status": "warning",
        },
        {
            "label": "Last Sync",
            "value": "-",
            "helper": "No sync detected",
            "status": "neutral",
        },
    ])
else:
    row = sync_status.iloc[0]

    status = row.get("status", "unknown")

    stat_row([
        {
            "label": "MT5 Sync",
            "value": status,
            "helper": row.get("message", ""),
            "status": "positive" if status == "connected" else "warning",
        },
        {
            "label": "Last Sync",
            "value": row.get("last_sync", "-"),
            "helper": "Desktop agent",
            "status": "neutral",
        },
    ])

section("System Health")

stat_row([
    {
        "label": "Trades",
        "value": health["trade_count"],
        "helper": AppHealthEngine.status_label(health["trades_loaded"]),
        "status": AppHealthEngine.status_colour(health["trades_loaded"]),
    },
    {
        "label": "Reviews",
        "value": health["review_count"],
        "helper": "Journal records",
        "status": "positive" if health["review_count"] > 0 else "warning",
    },
    {
        "label": "Screenshots",
        "value": health["screenshot_count"],
        "helper": "Visual journal files",
        "status": "positive" if health["screenshot_count"] > 0 else "warning",
    },
    {
        "label": "Replays",
        "value": health["replay_count"],
        "helper": "Replay notes",
        "status": "positive" if health["replay_count"] > 0 else "warning",
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
