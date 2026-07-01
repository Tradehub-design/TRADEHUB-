import streamlit as st


class UI:
    @staticmethod
    def header(title: str, subtitle: str = ""):
        st.markdown(
            f"""
            <div class="v4-topbar">
                <div>
                    <div class="v4-title">{title}</div>
                    <div class="v4-subtitle">{subtitle}</div>
                </div>
                <div class="v4-actions">
                    <div class="v4-action">Export PDF</div>
                    <div class="v4-action">Export CSV</div>
                    <div class="v4-action">⋯</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def section(title: str):
        st.markdown(f'<div class="v4-section">{title}</div>', unsafe_allow_html=True)

    @staticmethod
    def kpi(label: str, value, helper: str = "", status: str = "green"):
        st.markdown(
            f"""
            <div class="v4-card">
                <div class="v4-label">{label}</div>
                <div class="v4-value">{value}</div>
                <div class="v4-helper {status}">{helper}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def card(title: str, body: str, footer: str = ""):
        st.markdown(
            f"""
            <div class="v4-card">
                <div class="v4-label">{title}</div>
                <div style="margin-top:10px;">{body}</div>
                <div class="muted" style="margin-top:10px;font-size:13px;">{footer}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
