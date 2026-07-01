import streamlit as st

from core.ui import load_css, app_header

load_css()

app_header(

    "📄 Reports",

    "Professional trading reports."

)

st.button(

    "Generate Weekly Report"

)

st.button(

    "Generate Monthly Report"

)

st.button(

    "Generate Annual Report"

)
