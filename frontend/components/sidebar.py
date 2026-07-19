"""
Enterprise Sidebar

AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class SidebarComponent:

    @staticmethod
    def render():

        with st.sidebar:

            st.title("🤖 AI Data Analyst")

            st.caption(
                "Enterprise AI Business Intelligence"
            )

            st.divider()

            # ----------------------------------------
            # Dataset Status
            # ----------------------------------------

            st.subheader("📊 Dataset")

            if st.session_state.get(
                "upload_success",
                False,
            ):

                st.success("Dataset Loaded")

                st.write(
                    f"**File:** {st.session_state.get('file_name')}"
                )

                st.write(
                    f"**Rows:** {st.session_state.get('rows',0):,}"
                )

                st.write(
                    f"**Columns:** {st.session_state.get('columns',0)}"
                )

            else:

                st.info(
                    "No dataset uploaded."
                )

            st.divider()

            # ----------------------------------------
            # Recent Questions
            # ----------------------------------------

            st.subheader("🕒 Recent Questions")

            history = st.session_state.get(
                "history",
                [],
            )

            if history:

                for question in history[-5:]:

                    st.caption(f"• {question}")

            else:

                st.caption(
                    "No questions yet."
                )

            st.divider()

            # ----------------------------------------
            # AI Status
            # ----------------------------------------

            st.subheader("🤖 AI Status")

            st.success("AI Ready")

            st.caption("Gemini 2.5 Flash")

            st.divider()

            st.caption(
                "Version 1.0"
            )