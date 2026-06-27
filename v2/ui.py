import streamlit as st


class V2UI:

    @staticmethod
    def header(title, subtitle=""):
        st.markdown(
            f"""
            <div class="v2-header">
                <div>
                    <div class="v2-title">{title}</div>
                    <div class="v2-subtitle">{subtitle}</div>
                </div>
                <div class="quick-actions">
                    <div class="quick-action">Export PDF</div>
                    <div class="quick-action">Export CSV</div>
                    <div class="quick-action">⋯</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def section(title):
        st.markdown(
            f'<div class="v2-section">{title}</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def kpi(label, value, helper="", status="green"):
        st.markdown(
            f"""
            <div class="v2-card">
                <div class="v2-label">{label}</div>
                <div class="v2-value">{value}</div>
                <div class="{status}">{helper}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def card(title, body, footer=""):
        st.markdown(
            f"""
            <div class="v2-card">
                <div class="v2-label">{title}</div>
                <div style="margin-top:10px;">{body}</div>
                <div class="muted" style="margin-top:10px;font-size:13px;">{footer}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
