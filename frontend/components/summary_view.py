import streamlit as st


class SummaryView:
    """
    Displays the AI-generated business summary.
    """

    @staticmethod
    def render():

        summary = st.session_state.get("summary", "")

        if not summary:
            return

        st.subheader("📋 Business Summary")

        with st.container(border=True):

            st.markdown(summary)