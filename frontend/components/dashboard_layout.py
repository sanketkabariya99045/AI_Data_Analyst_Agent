"""
dashboard_layout.py

Enterprise dashboard layout for
AI Business Intelligence Platform.

Author:
Sanket Kabariya
"""

import streamlit as st


class DashboardLayout:
    """
    Creates the overall dashboard structure.
    """

    @staticmethod
    def render_header():

        st.set_page_config(
            page_title="AI Business Intelligence Platform",
            page_icon="📊",
            layout="wide",
        )

        st.title("📊 AI Business Intelligence Platform")

        st.caption(
            "Enterprise AI-powered Business Intelligence Platform"
        )

        st.divider()

    # ----------------------------------------------------

    @staticmethod
    def create_sections():

        upload_section = st.container()

        question_section = st.container()

        dataset_section = st.container()

        kpi_section = st.container()

        sql_section = st.container()

        result_section = st.container()

        summary_section = st.container()

        chart_section = st.container()

        download_section = st.container()
        
        history_section = st.container()

        return {
            "upload": upload_section,
            "question": question_section,
            "dataset": dataset_section,
            "kpis": kpi_section,
            "sql": sql_section,
            "result": result_section,
            "summary": summary_section,
            "chart": chart_section,
            "downloads": download_section,
            "history": history_section,
        }


dashboard_layout = DashboardLayout()