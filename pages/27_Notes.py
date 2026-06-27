import streamlit as st

from core.ui import load_css, app_header, section

load_css()

app_header(

    "📝 Notes",

    "Attach detailed notes to every trade."

)

section("Trade Notes")

st.text_input("Title")

st.text_area(

    "Notes",

    height=300

)

st.button("Save Note")

st.info(

    "Database saving will be enabled once Supabase is connected."

)
