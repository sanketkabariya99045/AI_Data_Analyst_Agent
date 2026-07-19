"""
Premium KPI Styles

Author:
Sanket Kabariya
"""

import streamlit as st


def load():

    st.markdown(
        """
<style>

/* KPI CARD */

.kpi-card{

background:white;

padding:22px;

border-radius:18px;

border:1px solid #E5E7EB;

box-shadow:0 3px 12px rgba(0,0,0,.08);

transition:.25s;

min-height:180px;
height:auto;

display:flex;

flex-direction:column;

justify-content:space-between;

}

.kpi-card:hover{

transform:translateY(-4px);

box-shadow:0 8px 22px rgba(0,0,0,.15);

}

.kpi-title{

font-size:18px;

font-weight:600;

color:#374151;

}

.kpi-value{

font-size:40px;

font-weight:700;

margin-top:12px;

margin-bottom:12px;

}

.kpi-description{

font-size:14px;

color:#6B7280;

}

</style>
""",
        unsafe_allow_html=True,
    )