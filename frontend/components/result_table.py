"""
frontend/components/result_table.py

Interactive Query Result Viewer.

Responsibilities
----------------
• Display SQL query results
• Show number of returned records
• Allow CSV download

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


class ResultTable:
    """
    SQL Result Table Component.
    """

    def render(self) -> None:
        """
        Display query results.
        """

        if "analysis" not in st.session_state:
            return

        response = st.session_state["analysis"]

        results = response.get("query_result", [])

        if not results:
            return

        df = pd.DataFrame(results)

        st.divider()

        st.subheader("📋 Query Results")

        col1, col2 = st.columns([1, 4])

        with col1:

            st.metric(
                "Rows Returned",
                len(df),
            )

        with col2:

            st.caption(
                "Results returned by the generated SQL query."
            )

        st.dataframe(
            df,
            width="stretch",
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Results (CSV)",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
            width="stretch",
        )