"""
Reusable Enterprise Card

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st


class Card:

    @staticmethod
    def render(
        *,
        title: str,
        value: str,
        icon: str,
        description: str = "",
        color: str = "#2563EB",
    ):

        st.markdown(
            f"""
<div style="
background:linear-gradient(180deg,#1E293B,#0F172A);
border-left:6px solid {color};
border-radius:18px;
padding:22px;
min-height:180px;
height:auto;
box-shadow:0 8px 24px rgba(0,0,0,.25);
overflow:hidden;
">

<div style="
font-size:18px;
font-weight:600;
color:white;
margin-bottom:18px;
">

{icon} {title}

</div>

<div style="
font-size:38px;
font-weight:700;
color:white;
margin-bottom:16px;
word-break:break-word;
">

{value}

</div>

<div style="
font-size:15px;
line-height:1.6;
color:#CBD5E1;
white-space:pre-wrap;
word-break:break-word;
">

{description}

</div>

</div>
""",
            unsafe_allow_html=True,
        )