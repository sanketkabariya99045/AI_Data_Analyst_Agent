import streamlit as st

from services.api_client import APIClient


class QuestionBox:

    @staticmethod
    def render():

        st.subheader("Ask Your Question")

        if not st.session_state.uploaded:

            st.info("Upload a dataset before asking questions.")

            return

        question = st.text_area(
            label="Question",
            placeholder="Example: Show total sales by category",
            value=st.session_state.question,
            height=100,
        )

        col1, col2 = st.columns([1, 5])

        with col1:

            analyze_clicked = st.button(
                "Analyze",
                type="primary",
                width="stretch",
            )

        if analyze_clicked:

            if not question.strip():

                st.warning("Please enter a question.")

                return

            st.session_state.question = question

            try:

                with st.spinner("AI is analyzing your data..."):

                    response = APIClient.analyze(question)

                st.session_state.generated_sql = response.get(
                    "generated_sql",
                    ""
                )

                st.session_state.summary = response.get(
                    "summary",
                    ""
                )

                st.session_state.report = response.get(
                    "executive_report",
                    {}
                )

                st.session_state.chart = response.get(
                    "chart",
                    None
                )

                st.session_state.query_result = response.get(
                    "query_result",
                    None
                )

                st.success("Analysis completed successfully!")

                st.rerun()

            except Exception as e:

                st.error(f"Analysis failed.\n\n{e}")