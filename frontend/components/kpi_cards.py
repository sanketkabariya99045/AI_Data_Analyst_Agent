"""
Premium KPI Cards

Enterprise Dashboard

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from styles.formatter import Formatter
from styles.icons import KPI_ICONS
from components.ui.card import Card


class KPICards:
    """
    Premium KPI Dashboard
    """

    # -----------------------------------------------------

    @staticmethod
    def _icon(name: str) -> str:

        lower = name.lower()

        for keyword, icon in KPI_ICONS.items():

            if keyword in lower:
                return icon

        return "📌"

    # -----------------------------------------------------

    @staticmethod
    def _color(name: str) -> str:

        lower = name.lower()

        if "sales" in lower:
            return "#2563EB"      # Blue

        if "profit" in lower:
            return "#16A34A"      # Green

        if "customer" in lower:
            return "#9333EA"      # Purple

        if "order" in lower:
            return "#EA580C"      # Orange

        if "quantity" in lower:
            return "#0891B2"      # Cyan

        if "discount" in lower:
            return "#DC2626"      # Red

        return "#64748B"

    # -----------------------------------------------------

    @staticmethod
    def _status(name: str, value):

        lower = name.lower()

        if "profit" in lower:

            if isinstance(value, (int, float)):

                return "🟢 Positive" if value >= 0 else "🔴 Negative"

        if "discount" in lower:
            return "🏷️ Average"

        if "sales" in lower:
            return "📈 Revenue"

        if "customer" in lower:
            return "👥 Customers"

        if "order" in lower:
            return "📦 Orders"

        return "● KPI"

    # -----------------------------------------------------

    @classmethod
    def render(cls):

        kpis = st.session_state.get("kpis", [])

        if not kpis:

            st.info("No KPI data available.")

            return

        st.subheader("📊 Business KPIs")

        # -----------------------------
        # Responsive Layout
        # -----------------------------

        if len(kpis) <= 2:

            cols = st.columns(len(kpis))

        elif len(kpis) <= 4:

            cols = st.columns(4)

        elif len(kpis) <= 6:

            cols = st.columns(3)

        else:

            cols = st.columns(4)

        # -----------------------------
        # Render Cards
        # -----------------------------

        for index, kpi in enumerate(kpis):

            with cols[index % len(cols)]:

                value = kpi.get("value")

                Card.render(

                    title=kpi.get("name", "KPI"),

                    value=Formatter.compact(value),

                    icon=cls._icon(kpi.get("name", "")),

                    description=kpi.get(
                        "description",
                        "",
                    ),

                    color=cls._color(
                        kpi.get("name", "")
                    ),

                )