import streamlit as st

from v2.navigation import V2Navigation
from v2.style import V2Style
from v2.ui import V2UI


st.set_page_config(
    page_title="TradeHub V2",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

V2Style.load()

selected = V2Navigation.sidebar()

V2UI.header(
    selected,
    "TradeHub V2 workspace"
)

st.info(
    "V2 navigation is active. Next step: build the Dashboard workspace."
)
