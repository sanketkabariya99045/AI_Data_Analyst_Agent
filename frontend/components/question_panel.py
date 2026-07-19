"""
frontend/components/question_panel.py

Enterprise Question Panel

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from services.api_client import APIClient


class QuestionPanel:

    def __init__(self):

        self.api = APIClient()

    # -------------------------------------------------

    def render(self):

        st.subheader("🤖 Ask Your Business Question")

        # -------------------------------------------------
        # Keep previous question
        # -------------------------------------------------

        default_question = st.session_state.get(
            "question",
            "",
        )

        question = st.text_input(
            "Ask anything about your data...",
            value=default_question,
            placeholder="Example: Which category has the highest sales?",
            key="question_input",
        )

        # Keep session updated
        st.session_state["question"] = question

        # -------------------------------------------------
        # Automatic execution from AI Suggestions
        # -------------------------------------------------

        if st.session_state.get("run_analysis", False):

            st.session_state["run_analysis"] = False

            if question.strip():

                self.run_pipeline(question)

            return

        # -------------------------------------------------
        # Manual Analyze Button
        # -------------------------------------------------

        if st.button(
            "🚀 Analyze",
            width="stretch",
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

                return

            self.run_pipeline(question)

    # -------------------------------------------------

    def run_pipeline(
        self,
        question: str,
    ):

        progress = st.progress(0)

        status = st.empty()

        try:

            # -----------------------------------------

            status.info("🧠 Understanding your question...")

            progress.progress(10)

            # -----------------------------------------

            status.info("🤖 Generating SQL...")

            progress.progress(25)

            history = st.session_state.get(
                "history",
                [],
            )

            history.append(question)

            st.session_state["history"] = history

            # -----------------------------------------

            response = self.api.analyze(
                question,
            )

            # -----------------------------------------

            status.info("🗄 Executing SQL Query...")

            progress.progress(55)

            # -----------------------------------------

            st.session_state["generated_sql"] = response.get(
                "generated_sql",
                "",
            )

            st.session_state["query_result"] = response.get(
                "query_result",
                [],
            )

            st.session_state["summary"] = response.get(
                "summary",
                {},
            )
            
            st.session_state["executive_summary"] = response.get(
                "executive_summary",
                "",
            )

            st.session_state["explanation"] = response.get(
                "explanation",
                {},
            )

            st.session_state["chart"] = response.get(
                "chart",
                None,
            )

            st.session_state["kpis"] = response.get(
                "kpis",
                [],
            )

            st.session_state["trends"] = response.get(
                "trends",
                [],
            )

            st.session_state["anomalies"] = response.get(
                "anomalies",
                [],
            )

            st.session_state["recommendations"] = response.get(
                "recommendations",
                [],
            )

            st.session_state["statistics"] = response.get(
                "statistics",
                [],
            )

            st.session_state["insights"] = response.get(
                "insights",
                [],
            )

            st.session_state["warnings"] = response.get(
                "warnings",
                [],
            )
            
            # -----------------------------------------

            status.info("📊 Building Business Insights...")

            progress.progress(80)

            # -----------------------------------------

            status.info("🎨 Rendering Dashboard...")

            progress.progress(95)

            # -----------------------------------------

            status.success(
                "✅ Analysis Complete!"
            )

            progress.progress(100)

            st.rerun()

        except Exception as error:

            status.error(str(error))

            progress.empty()