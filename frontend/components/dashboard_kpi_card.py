"""
Enterprise Dashboard KPI Card

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class DashboardKPICard:

    COLORS = [
        "#2563EB",
        "#059669",
        "#DC2626",
        "#7C3AED",
        "#EA580C",
        "#0891B2",
        "#65A30D",
        "#DB2777",
    ]

    @classmethod
    def render(
        cls,
        title: str,
        value,
        description: str = "",
        index: int = 0,
    ):

        color = cls.COLORS[
            index % len(cls.COLORS)
        ]

        st.markdown(
            f"""
<div style="
background:white;
border-left:7px solid {color};
border-radius:18px;
padding:22px;
height:180px;
box-shadow:0 6px 16px rgba(0,0,0,.08);
">

<div style="
font-size:17px;
font-weight:600;
color:#374151;
">

{title}

</div>

<div style="
font-size:34px;
font-weight:700;
margin-top:18px;
color:{color};
">

{value}

</div>

<div style="
margin-top:18px;
font-size:13px;
color:#6B7280;
">

{description}

</div>

</div>
""",
            unsafe_allow_html=True,
        )