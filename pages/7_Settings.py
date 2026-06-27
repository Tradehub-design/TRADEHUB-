import streamlit as st

from core.ui import load_css, app_header

load_css()

app_header(

    "⚙ Settings",

    "Configure TradeHub."

)

tab1, tab2, tab3 = st.tabs([

    "General",

    "Trading",

    "Database"

])

with tab1:

    st.toggle(

        "Dark Mode",

        value=True

    )

    st.toggle(

        "Animations",

        value=True

    )

with tab2:

    st.number_input(

        "Default Risk %",

        value=1.0

    )

    st.selectbox(

        "Default Session",

        [

            "Asia",

            "London",

            "New York"

        ]

    )

with tab3:

    st.text_input(

        "Supabase URL"

    )

    st.text_input(

        "Supabase Key",

        type="password"

    )

    st.button(

        "Test Connection"

    )
