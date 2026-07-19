"""
frontend/pages/dashboard.py

AI Dashboard Builder Page.

Allows users to generate complete
business dashboards using natural language.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from services.dashboard_api import (
    dashboard_api,
)

from components.dashboard_renderer import (
    DashboardRenderer,
)


class DashboardPage:
    """
    AI Dashboard Builder Page.
    """

    def render(self):

        st.title("📊 AI Dashboard Builder")

        st.markdown(
            """
Generate an executive business dashboard from
a single natural language prompt.
"""
        )

        st.divider()

        # --------------------------------------------------
        # User Input
        # --------------------------------------------------

        question = st.text_input(

            "Dashboard Request",

            placeholder=(
                "Example: Create a Sales Dashboard"
            ),

        )

        # --------------------------------------------------
        # Build Dashboard
        # --------------------------------------------------

        if st.button(

            "🚀 Build Dashboard",

            width="stretch",

        ):

            if not question.strip():

                st.warning(
                    "Please enter a dashboard request."
                )

                return

            with st.spinner(
                "Building AI Dashboard..."
            ):

                try:

                    response = dashboard_api.build_dashboard(
                        question,
                    )

                    st.session_state[
                        "dashboard"
                    ] = response

                    st.success(
                        "Dashboard generated successfully!"
                    )

                except Exception as error:

                    st.error(
                        str(error)
                    )

        st.divider()

        # --------------------------------------------------
        # Render Dashboard
        # --------------------------------------------------

        DashboardRenderer.render()