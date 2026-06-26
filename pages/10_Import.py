import streamlit as st
import pandas as pd

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe
from data.data_engine import DataEngine


load_css()

app_header(
    "📥 Import Centre",
    "Import MT5 history and prepare TradeHub for
