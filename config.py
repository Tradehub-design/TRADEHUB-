import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# General settings
APP_NAME = "TradeHub"
TIMEZONE = "Australia/Sydney"

# Default currency
BASE_CURRENCY = "AUD"

# Dashboard settings
DEFAULT_PAGE_SIZE = 50

# Risk settings
DEFAULT_RISK_PERCENT = 1.0

# Screenshot settings
SCREENSHOT_FOLDER = "screenshots"

# MT5 settings
MT5_PATH = ""
MT5_LOGIN = ""
MT5_SERVER = ""
MT5_PASSWORD = ""
