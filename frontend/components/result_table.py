"""
frontend/components/result_table.py

Enterprise Result Workspace

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from state.dashboard_state import DashboardState

class ResultTable:
    """
    Enterprise Query Result Workspace.
    """

    @staticmethod
    def render():

        data = DashboardState.results()

        if not data:

            return

        df = pd.DataFrame(data)

        st.subheader("📄 Query Results")

        # ===================================================
        # Dataset Statistics
        # ===================================================

        rows = len(df)

        cols = len(df.columns)

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Rows",
                f"{rows:,}",
            )

        with c2:

            st.metric(
                "Columns",
                cols,
            )

        with c3:

            st.metric(
                "Memory",
                f"{round(df.memory_usage(deep=True).sum()/1024,1)} KB",
            )

        st.divider()

        # ===================================================
        # Search
        # ===================================================

        search = st.text_input(
            "🔍 Search results",
            key="result_search",
            placeholder="Search any value...",
        )

        if search:

            mask = df.astype(str).apply(

                lambda column: column.str.contains(
                    search,
                    case=False,
                    na=False,
                )

            )

            df = df[mask.any(axis=1)]

        # ===================================================
        # Interactive Table
        # ===================================================

        st.dataframe(

            df,

            width="stretch",

            hide_index=True,

            height=450,

        )

        st.caption(
            f"Showing {len(df):,} of {rows:,} rows"
        )

        st.divider()

        # ===================================================
        # Downloads
        # ===================================================

        csv = df.to_csv(
            index=False,
        )

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(

                "⬇ Download CSV",

                csv,

                "query_results.csv",

                "text/csv",

                width="stretch",

            )

        with col2:

            st.download_button(

                "⬇ Download JSON",

                df.to_json(
                    orient="records",
                    indent=2,
                ),

                "query_results.json",

                "application/json",

                width="stretch",

            )