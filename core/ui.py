import streamlit as st


def load_css():
    try:
        with open("assets/styles.css", "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


def app_header(title, subtitle=""):
    st.markdown(
        f"""
        <div class="app-hero">
            <div>
                <div class="app-hero-title">{title}</div>
                <div class="app-hero-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section(title):
    st.markdown(
        f"""
        <div class="section-title">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


def metric(label, value, helper="", status="neutral"):
    status_class = {
        "positive": "metric-positive",
        "negative": "metric-negative",
        "neutral": "metric-neutral",
        "warning": "metric-warning",
    }.get(status, "metric-neutral")

    st.markdown(
        f"""
        <div class="premium-card metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value {status_class}">{value}</div>
            <div class="metric-helper">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight(title, body):
    st.markdown(
        f"""
        <div class="premium-card insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def badge(text):
    st.markdown(
        f"""
        <span class="tradehub-badge">{text}</span>
        """,
        unsafe_allow_html=True
    )


def card(title, body="", footer=""):
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">{title}</div>
            <div class="card-body">{body}</div>
            <div class="card-footer">{footer}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def divider():
    st.markdown(
        '<div class="tradehub-divider"></div>',
        unsafe_allow_html=True
    )
