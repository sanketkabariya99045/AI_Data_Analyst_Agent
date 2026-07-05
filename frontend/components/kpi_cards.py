"""
frontend/components/kpi_cards.py

Professional KPI Cards.

Displays important business metrics returned
from the AI Analysis Engine.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class KPICards:
    """
    Professional KPI Cards.
    """

    def render(self) -> None:
        """
        Render KPI cards.
        """

        if "analysis" not in st.session_state:
            return

        response = st.session_state["analysis"]

        kpis = response.get("kpis", [])

        if not kpis:

            return

        st.divider()

        st.subheader("📈 Key Performance Indicators")

        columns = st.columns(
            min(
                len(kpis),
                4,
            )
        )

        for index, kpi in enumerate(kpis):

            with columns[index % len(columns)]:

                value = kpi.get(
                    "value",
                    "-"
                )

                delta = kpi.get(
                    "change_percentage"
                )

                description = kpi.get(
                    "description",
                    ""
                )

                st.metric(

                    label=kpi.get(
                        "name",
                        "KPI",
                    ),

                    value=value,

                    delta=(
                        f"{delta:.2f}%"
                        if delta is not None
                        else None
                    ),
                )

                if description:

                    st.caption(
                        description
                    )