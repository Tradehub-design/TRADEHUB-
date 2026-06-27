import os
from dotenv import load_dotenv


load_dotenv()


class DesktopSyncConfig:

    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

    MT5_LOGIN = os.getenv("MT5_LOGIN", "")
    MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
    MT5_SERVER = os.getenv("MT5_SERVER", "")

    BROKER_NAME = os.getenv("BROKER_NAME", "Fusion Markets")
    ACCOUNT_CURRENCY = os.getenv("ACCOUNT_CURRENCY", "AUD")

    SYNC_INTERVAL_SECONDS = int(
        os.getenv("SYNC_INTERVAL_SECONDS", "60")
    )

    HISTORY_DAYS_BACK = int(
        os.getenv("HISTORY_DAYS_BACK", "60")
    )
