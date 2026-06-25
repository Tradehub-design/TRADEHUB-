import streamlit as st


def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def page_header(title, subtitle=""):
    st.markdown(
        f"""
        <div class="tradehub-title">{title}</div>
        <div class="tradehub-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )


def card(content):
    st.markdown(
        f"""
        <div class="tradehub-card">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(label, value, status="neutral"):
    css_class = {
        "positive": "metric-positive",
        "negative": "metric-negative",
        "neutral": "metric-neutral",
    }.get(status, "metric-neutral")

    st.markdown(
        f"""
        <div class="tradehub-card">
            <div style="color:#A1A1AA;font-size:13px;">{label}</div>
            <div class="{css_class}" style="font-size:24px;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def badge(text):
    st.markdown(
        f'<span class="badge">{text}</span>',
        unsafe_allow_html=True
    )
