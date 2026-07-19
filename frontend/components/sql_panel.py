"""
frontend/components/sql_panel.py

Enterprise SQL Workspace

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from state.dashboard_state import DashboardState

class SQLPanel:
    """
    Enterprise SQL Workspace.
    """

    @staticmethod
    def render():

        sql = DashboardState.sql()

        if not sql:

            return

        st.subheader("💻 SQL Workspace")

        # =====================================
        # Metadata
        # =====================================

        execution_time = st.session_state.get(
            "execution_time",
            None,
        )

        rows = len(
            st.session_state.get(
                "query_result",
                [],
            )
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.success("✅ SQL Valid")

        with col2:

            if execution_time is not None:

                st.info(
                    f"⏱ {execution_time:.3f} sec"
                )

            else:

                st.info("⏱ --")

        with col3:

            st.info(
                f"📄 {rows} Rows"
            )

        st.divider()

        # =====================================
        # SQL Viewer
        # =====================================

        st.code(
            sql,
            language="sql",
        )

        st.caption("Database Engine: DuckDB")

        st.divider()

        # =====================================
        # Actions
        # =====================================

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(

                "⬇ Download SQL",

                sql,

                file_name="generated_query.sql",

                mime="text/plain",

                width="stretch",

            )

        with col2:

            st.code(
                "Ctrl + C",
                language="text",
            )

            st.caption(
                "Copy directly from the SQL editor."
            )