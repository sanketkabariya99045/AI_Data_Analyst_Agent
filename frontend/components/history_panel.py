"""
frontend/components/history_panel.py

Enterprise Query History Panel

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class HistoryPanel:
    """
    Displays AI query history.
    """

    @staticmethod
    def render():

        st.subheader("🕒 Query History")

        history = st.session_state.get(
            "history",
            [],
        )

        if not history:

            st.info("No questions asked yet.")
            return

        for i, question in enumerate(
            reversed(history),
            start=1,
        ):

            with st.expander(
                f"{i}. {question}"
            ):

                st.write(question)

        if st.button(
            "🗑 Clear History",
            width="stretch",
        ):

            st.session_state.history = []

            st.rerun()