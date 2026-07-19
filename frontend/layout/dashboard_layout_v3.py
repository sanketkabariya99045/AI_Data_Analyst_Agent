"""
Dashboard Layout V3

Enterprise Layout

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class DashboardLayoutV3:

    @staticmethod
    def header():

        st.title("🤖 AI Business Intelligence Platform")

        st.caption(
            "Natural Language → SQL → AI Insights → Dashboard"
        )

        st.divider()

    # ------------------------------------------------

    @staticmethod
    def landing():

        return st.columns(
            [1, 2],
            gap="large",
        )

    # ------------------------------------------------

    @staticmethod
    def analytics():

        return st.columns(
            [2, 1],
            gap="large",
        )

    # ------------------------------------------------

    @staticmethod
    def workspace():

        return st.columns(
            [1, 2],
            gap="large",
        )


dashboard_layout_v3 = DashboardLayoutV3()