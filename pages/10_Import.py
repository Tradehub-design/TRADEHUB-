import streamlit as st

from core.ui import load_css, app_header, section

load_css()

app_header(

    "📥 Import Centre",

    "Everything enters TradeHub from here."

)

section("MT5")

st.button("Import MT5 History")

section("CSV")

st.file_uploader(

    "CSV Import",

    type=["csv"]

)

section("TradingView")

st.file_uploader(

    "TradingView Export"

)

section("Screenshots")

st.file_uploader(

    "Upload Images",

    accept_multiple_files=True

)

section("Import Status")

st.success(

    "Ready for MT5 Sync Agent."

)
