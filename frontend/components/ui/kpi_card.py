"""
Enterprise KPI Card

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class KPICard:

    @staticmethod
    def render(
        *,
        title: str,
        value,
        description: str = "",
        color: str = "#2563EB",
    ):

        # -------------------------------------
        # Number Formatting
        # -------------------------------------

        if isinstance(value, (int, float)):

            if abs(value) >= 1_000_000_000:
                value = f"{value/1_000_000_000:.2f}B"

            elif abs(value) >= 1_000_000:
                value = f"{value/1_000_000:.2f}M"

            elif abs(value) >= 1_000:
                value = f"{value/1_000:.2f}K"

            else:
                value = f"{value:.2f}"

        st.markdown(
            f"""
<div style="
background:linear-gradient(180deg,#1E293B,#0F172A);
border-left:6px solid {color};
border-radius:18px;
padding:22px;
min-height:165px;
display:flex;
flex-direction:column;
justify-content:space-between;
box-shadow:0 8px 24px rgba(0,0,0,.25);
">

<div style="
font-size:16px;
font-weight:600;
color:#CBD5E1;
">

{title}

</div>

<div style="
font-size:36px;
font-weight:700;
color:white;
margin-top:20px;
">

{value}

</div>

<div style="
margin-top:16px;
font-size:14px;
color:#94A3B8;
">

{description}

</div>

</div>
""",
            unsafe_allow_html=True,
        )