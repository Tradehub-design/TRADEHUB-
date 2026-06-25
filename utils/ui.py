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


def section_title(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


def metric_card(label, value, status="neutral"):
    status_class = {
        "positive": "metric-positive",
        "negative": "metric-negative",
        "neutral": "metric-neutral",
    }.get(status, "metric-neutral")

    st.markdown(
        f"""
        <div class="tradehub-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value {status_class}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def info_card(title, body):
    st.markdown(
        f"""
        <div class="tradehub-card">
            <div style="font-size:17px;font-weight:800;margin-bottom:8px;">{title}</div>
            <div style="color:#A1A1AA;font-size:14px;line-height:1.5;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def badge(text):
    st.markdown(
        f'<span class="badge">{text}</span>',
        unsafe_allow_html=True
    )
