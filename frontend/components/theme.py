"""
theme.py

Loads custom CSS.

Author:
Sanket Kabariya
"""

import streamlit as st
from pathlib import Path

class Theme:

    @staticmethod
    def load():

        BASE_DIR = Path(__file__).resolve().parent.parent
        CSS_FILE = BASE_DIR / "assets" / "style.css"

        with open(CSS_FILE, encoding="utf-8") as css:
            st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

        