"""
Global CSS

Enterprise Design System

Author:
Sanket Kabariya
"""

import streamlit as st


def load():

    st.markdown(
        """
<style>

/* ---------- GLOBAL ---------- */

.main .block-container{

    max-width:1400px;

    padding-top:2rem;

    padding-bottom:2rem;

}

/* ---------- HEADINGS ---------- */

h1{

    font-size:2.2rem;

    font-weight:700;

}

h2{

    font-weight:600;

}

h3{

    font-weight:600;

}

/* ---------- KPI CARD ---------- */

.kpi-card{

    background:white;

    border-radius:18px;

    border:1px solid #E5E7EB;

    padding:22px;

    box-shadow:0 6px 16px rgba(0,0,0,.08);

    transition:all .25s ease;

    min-height:180px;

}

.kpi-card:hover{

    transform:translateY(-6px);

    box-shadow:0 12px 28px rgba(0,0,0,.16);

}

/* ---------- SECTION CARD ---------- */

.section-card{

    background:white;

    border-radius:18px;

    border:1px solid #ECECEC;

    padding:24px;

    margin-bottom:20px;

}

/* ---------- SQL ---------- */

.sql-card{

    background:#111827;

    color:white;

    border-radius:12px;

    padding:18px;

}

/* ---------- DATASET HEALTH ---------- */

.health-card{

    border-left:6px solid #16a34a;

}

/* ---------- SCROLL ---------- */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#c7c7c7;

    border-radius:12px;

}

</style>
""",
        unsafe_allow_html=True,
    )