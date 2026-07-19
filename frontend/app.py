"""
frontend/app.py

Enterprise AI Business Intelligence Platform

Application Entry Point

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from utils.session import initialize_session

from components.theme import Theme
from components.sidebar import SidebarComponent

from dashboard.main_dashboard import (
    MainDashboard,
)

from pages.dashboard import (
    DashboardPage,
)

from styles.css import load as load_css


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="AI Business Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# Initialize Application
# ==========================================================

initialize_session()

Theme.load()
load_css()

# ==========================================================
# Navigation
# ==========================================================

with st.sidebar:

    st.title("📊 AI BI Platform")

    st.markdown("---")

    page = st.radio(

        "Navigation",

        [

            "📊 AI Data Analyst",

            "📈 AI Dashboard Builder",

        ],

    )

# ==========================================================
# Pages
# ==========================================================

if page == "📊 AI Data Analyst":

    SidebarComponent.render()

    dashboard = MainDashboard()

    dashboard.render()

else:

    dashboard_builder = DashboardPage()

    dashboard_builder.render()