import streamlit as st


def command_card(title, body, footer=""):
    st.markdown(
        f"""
        <div class="pro-card">
            <div class="card-title">{title}</div>
            <div class="card-body">{body}</div>
            <div class="card-footer">{footer}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_row(items):
    cols = st.columns(len(items))

    for col, item in zip(cols, items):
        with col:
            status = item.get("status", "neutral")
            status_class = {
                "positive": "positive",
                "negative": "negative",
                "warning": "warning",
                "neutral": "neutral",
            }.get(status, "neutral")

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">{item.get("label", "")}</div>
                    <div class="metric-value {status_class}">
                        {item.get("value", "-")}
                    </div>
                    <div class="metric-helper">{item.get("helper", "")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def mini_card(title, value, helper="", status="neutral", icon=""):
    status_class = {
        "positive": "positive",
        "negative": "negative",
        "warning": "warning",
        "neutral": "neutral",
    }.get(status, "neutral")

    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-icon">{icon}</div>
            <div class="mini-title">{title}</div>
            <div class="mini-value {status_class}">{value}</div>
            <div class="mini-helper">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def table_header(title, subtitle=""):
    st.markdown(
        f"""
        <div class="table-header">
            <div>
                <div class="table-title">{title}</div>
                <div class="table-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(title, body, tag=""):
    tag_html = f'<span class="badge">{tag}</span>' if tag else ""

    st.markdown(
        f"""
        <div class="pro-card">
            {tag_html}
            <div class="card-title">{title}</div>
            <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def trade_quality_card(score, helper=""):
    if score >= 85:
        status = "positive"
        label = "Strong Edge"
    elif score >= 70:
        status = "warning"
        label = "Moderate Edge"
    else:
        status = "negative"
        label = "Weak Edge"

    st.markdown(
        f"""
        <div class="edge-panel">
            <div class="edge-circle">
                <div class="edge-number {status}">{score}</div>
                <div class="edge-total">/100</div>
            </div>
            <div class="edge-label">{label}</div>
            <div class="edge-helper">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_card(title, value, helper="", status="neutral", icon=""):
    status_class = {
        "positive": "positive",
        "negative": "negative",
        "warning": "warning",
        "neutral": "neutral",
    }.get(status, "neutral")

    st.markdown(
        f"""
        <div class="pro-card">
            <div class="mini-icon">{icon}</div>
            <div class="metric-label">{title}</div>
            <div class="metric-value {status_class}">{value}</div>
            <div class="metric-helper">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
