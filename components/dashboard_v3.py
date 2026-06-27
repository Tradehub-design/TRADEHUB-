import streamlit as st


class DashboardV3:

    @staticmethod
    def load_css():
        try:
            with open("assets/dashboard_v3.css", "r", encoding="utf-8") as file:
                st.markdown(
                    f"<style>{file.read()}</style>",
                    unsafe_allow_html=True
                )
        except FileNotFoundError:
            pass

    @staticmethod
    def kpi(label, value, helper="", status="green"):
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-helper {status}">{helper}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def panel(title):
        st.markdown(
            f"""
            <div class="panel-title">{title}</div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def side_card(title, body, footer=""):
        st.markdown(
            f"""
            <div class="side-card">
                <div class="panel-title">{title}</div>
                <div>{body}</div>
                <div style="color:#94a3b8;font-size:12px;margin-top:10px;">{footer}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def quick_menu():
        st.markdown(
            """
            <div class="quick-menu">
                <div class="quick-button">Export PDF</div>
                <div class="quick-button">Export CSV</div>
                <div class="quick-button">Monthly Report</div>
                <div class="quick-button">⋯</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
