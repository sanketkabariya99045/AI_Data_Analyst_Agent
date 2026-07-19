"""
frontend/components/summary_panel.py

Enterprise Executive Summary Dashboard

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from components.ui.card import Card
from state.dashboard_state import DashboardState

class SummaryPanel:
    """
    Executive Summary Dashboard.
    """

    def render(self):

        summary = DashboardState.summary()

        if not summary:

            return

        st.subheader("📋 Executive Summary")

        # =====================================
        # Executive Summary
        # =====================================

        executive = summary.get(
            "executive_summary",
            ""
        )

        if executive:

            Card.render(

                title="Executive Summary",

                value="🧠 AI",

                icon="📋",

                description=executive,

                color="#2563EB",


            )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================
        # Overview + Trend
        # =====================================

        col1, col2 = st.columns(2)

        with col1:

            overview = summary.get(
                "overview",
                ""
            )

            if overview:

                Card.render(

                    title="Overview",

                    value="📈",

                    icon="📊",

                    description=overview,

                    color="#16A34A",


                )

        with col2:

            trend = summary.get(
                "trend_summary",
                ""
            )

            if trend:

                Card.render(

                    title="Trend",

                    value="📈",

                    icon="🚀",

                    description=trend,

                    color="#0EA5E9",


                )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================
        # Risk + Recommendation
        # =====================================

        col1, col2 = st.columns(2)

        with col1:

            anomaly = summary.get(
                "anomaly_summary",
                ""
            )

            if anomaly:

                Card.render(

                    title="Risk Analysis",

                    value="⚠️",

                    icon="🛡️",

                    description=anomaly,

                    color="#F59E0B",

                )

        with col2:

            recommendations = summary.get(
                "recommendation_summary",
                [],
            )

            if recommendations:

                Card.render(

                    title="Recommendations",

                    value=f"{len(recommendations)}",

                    icon="💡",

                    description="\n".join(
                        f"• {item}"
                        for item in recommendations
                    ),

                    color="#8B5CF6",

                )