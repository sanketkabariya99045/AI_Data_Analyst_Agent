"""
frontend/components/dashboard_renderer.py

Enterprise Dashboard Renderer.

Renders AI-generated dashboards returned
by the backend.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

from components.ui.kpi_card import KPICard
class DashboardRenderer:
    """
    Renders a complete AI dashboard.
    """

    @staticmethod
    def render():

        dashboard = st.session_state.get(
            "dashboard",
        )

        if not dashboard:

            st.info(
                "Generate a dashboard to begin."
            )
            return

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        st.markdown(
            f"""
        # 📊 {dashboard["title"]}

        {dashboard["description"]}
        """
        )

        st.divider()

        # --------------------------------------------------
        # KPI Cards
        # --------------------------------------------------

        kpis = dashboard.get(
            "kpis",
            [],
        )

        if kpis:

            st.subheader("📊 Key Performance Indicators")

            column_count = min(
                4,
                max(
                    1,
                    len(kpis),
                ),
            )

            columns = st.columns(column_count)

            colors = [

                "#2563EB",  # Blue
                "#10B981",  # Green
                "#F59E0B",  # Orange
                "#8B5CF6",  # Purple

            ]

            for index, kpi in enumerate(kpis):

                with columns[index % 4]:

                    KPICard.render(

                        title=kpi["title"],

                        value=kpi["value"],

                        description=kpi.get(
                            "description",
                            "",
                        ),

                        color=colors[index % len(colors)],

                    )
        # --------------------------------------------------
        # Charts
        # --------------------------------------------------

        charts = dashboard.get(
            "charts",
            [],
        )

        if charts:

            st.subheader(
                "📈 Dashboard Visualizations"
            )

            cols = st.columns(2)

            for index, chart in enumerate(charts):

                with cols[index % 2]:

                    st.markdown(
                        f"#### {chart['title']}"
                    )

                    figure = go.Figure(
                        chart["chart"]
                    )

                    st.plotly_chart(
                        figure,
                        width="stretch",
                    )
        st.divider()
        
        # --------------------------------------------------
        # Tables
        # --------------------------------------------------

        tables = dashboard.get(
            "tables",
            [],
        )

        if tables:

            st.subheader("📋 Data Tables")

            for table in tables:

                st.markdown(
                    f"#### {table['title']}"
                )

                st.dataframe(
                    table["rows"],
                    width="stretch",
                    hide_index=True,
                )

            st.divider()
           
        # --------------------------------------------------
        # Executive Summary
        # --------------------------------------------------

        summary = dashboard.get(
            "summary",
        )

        if summary:

            st.subheader("📋 Executive Summary")

            with st.container(border=True):

                st.markdown(summary["overview"])

            recommendations = summary.get(
                "recommendations",
                [],
            )

            if recommendations:

                st.markdown(
                    "### 💡 Recommendations"
                )

                for recommendation in recommendations:

                    st.markdown(
                        f"- {recommendation}"
                    )

            risks = summary.get(
                "risks",
                [],
            )

            if risks:

                st.markdown(
                    "### ⚠️ Risks"
                )

                for risk in risks:

                    st.markdown(
                        f"- {risk}"
                    )

            opportunities = summary.get(
                "opportunities",
                [],
            )

            if opportunities:

                st.markdown(
                    "### 🚀 Opportunities"
                )

                for opportunity in opportunities:

                    st.markdown(
                        f"- {opportunity}"
                    )

        st.divider()

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = dashboard.get(
            "metadata",
            {},
        )

        if metadata:

            with st.expander(
                "Dashboard Metadata"
            ):

                st.json(
                    metadata
                )