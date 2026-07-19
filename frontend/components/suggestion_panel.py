"""
Enterprise AI Suggestion Panel

Displays AI-generated suggested questions.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class SuggestionPanel:

    ICONS = [
        "📈",
        "💰",
        "🌍",
        "👤",
        "📦",
        "📊",
        "🏆",
        "📅",
    ]

    # -----------------------------------------------------

    def render(self):

        suggestions = st.session_state.get(
            "suggestions",
            [],
        )

        if not suggestions:

            return

        st.subheader("💡 AI Suggested Questions")

        cols = st.columns(2)

        for i, suggestion in enumerate(suggestions):

            icon = self.ICONS[
                i % len(self.ICONS)
            ]

            question = suggestion.get(
                "question",
                "",
            )

            with cols[i % 2]:

                if st.button(

                    f"{icon} {question}",

                    key=f"suggestion_{i}",

                    width="stretch",

                ):

                    st.session_state["question"] = question

                    st.session_state["run_analysis"] = True

                    st.rerun()