import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

@st.cache_resource
def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("Missing Supabase URL or key. Add them to your .env file.")
        return None

    return create_client(SUPABASE_URL, SUPABASE_KEY)
