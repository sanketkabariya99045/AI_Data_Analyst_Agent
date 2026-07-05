"""
frontend/components/question_panel.py

Business Question Component.

Responsibilities
----------------
• Accept business questions
• Call AI Analyze API
• Store analysis response
• Handle loading/errors

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from services.api_client import APIClient


class QuestionPanel:
    """
    Business Question Panel.
    """

    def __init__(self) -> None:

        self.api = APIClient()

    # ---------------------------------------------------------

    def render(self) -> None:
        """
        Render question input.
        """

        st.subheader("💬 Ask Your Business Question")

        question = st.text_area(
            label="Question",
            placeholder="Example: Which category has the highest sales?",
            height=100,
            label_visibility="collapsed",
        )

        analyze = st.button(
            "🚀 Analyze",
            width="stretch",
            type="primary",
        )

        if not analyze:
            return

        if question.strip() == "":

            st.warning(
                "Please enter a business question."
            )

            return

        with st.spinner(
            "AI is analyzing your data..."
        ):

            try:

                response = self.api.analyze(
                    question
                )

                if response["success"]:

                    st.success(
                        "Analysis completed successfully."
                    )

                    st.session_state[
                        "analysis"
                    ] = response

                else:

                    st.error(
                        response.get(
                            "error",
                            "Analysis failed.",
                        )
                    )

            except Exception as error:

                st.error(str(error))