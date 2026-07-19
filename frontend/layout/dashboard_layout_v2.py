"""
Enterprise Dashboard Layout

Version 2

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class DashboardLayoutV2:

    def render_header(self):

        st.markdown(
            """
# 🤖 AI Business Intelligence Platform

Ask questions in natural language and receive
executive-level business insights powered by AI.
"""
        )

        st.divider()

    # -----------------------------------------------------

    def top_layout(self):

        left, right = st.columns(
            [1, 2],
            gap="large",
        )

        return left, right

    # -----------------------------------------------------

    def chart_layout(self):

        chart, summary = st.columns(
            [2, 1],
            gap="large",
        )

        return chart, summary

    # -----------------------------------------------------

    def bottom_layout(self):

        sql, table = st.columns(
            [1, 2],
            gap="large",
        )

        return sql, table


dashboard_layout_v2 = DashboardLayoutV2()