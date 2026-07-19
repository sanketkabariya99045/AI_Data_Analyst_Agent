"""
Enterprise AI Explanation Dashboard

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from components.ui.card import Card


class ExplanationPanel:
    """
    Premium AI Explanation Dashboard.
    """

    def render(self):

        explanation = st.session_state.get(
            "explanation",
            {},
        )

        if not explanation:

            return

        st.subheader("🤖 AI Business Explanation")

        # ===========================================
        # Overview
        # ===========================================

        overview = explanation.get(
            "overview",
            "",
        )

        if overview:

            Card.render(

                title="Overview",

                value="🧠",

                icon="🤖",

                description=overview,

                color="#2563EB",

            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ===========================================
        # Trend + Risk
        # ===========================================

        col1, col2 = st.columns(2)

        with col1:

            trends = explanation.get(
                "trends",
                "",
            )

            if trends:

                Card.render(

                    title="Business Trend",

                    value="📈",

                    icon="📊",

                    description=trends,

                    color="#16A34A",
                )

        with col2:

            risks = explanation.get(
                "risks",
                "",
            )

            if risks:

                Card.render(

                    title="Risk Analysis",

                    value="⚠️",

                    icon="🛡️",

                    description=risks,

                    color="#F59E0B",

    

                )

        st.markdown("<br>", unsafe_allow_html=True)

        # ===========================================
        # Opportunity + Recommendation
        # ===========================================

        col1, col2 = st.columns(2)

        with col1:

            opportunities = explanation.get(
                "opportunities",
                "",
            )

            if opportunities:

                Card.render(

                    title="Opportunities",

                    value="🚀",

                    icon="💼",

                    description=opportunities,

                    color="#0EA5E9",

                )

        with col2:

            recommendations = explanation.get(
                "recommendations",
                "",
            )

            if recommendations:

                Card.render(

                    title="Recommendations",

                    value="💡",

                    icon="🎯",

                    description=recommendations,

                    color="#8B5CF6",

                )

        # ===========================================
        # Conclusion
        # ===========================================

        conclusion = explanation.get(
            "conclusion",
            "",
        )

        if conclusion:

            st.markdown("<br>", unsafe_allow_html=True)

            Card.render(

                title="Final Conclusion",

                value="✅",

                icon="📋",

                description=conclusion,

                color="#10B981",


            )