import streamlit as st

from core.ui import load_css, app_header

load_css()

app_header(

    "🔬 Research Lab",

    "Store ideas before risking money."

)

st.text_area(

    "Market Thesis",

    height=300

)

st.button(

    "Save Research"

)
