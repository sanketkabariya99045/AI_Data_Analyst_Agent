"""
theme.py

Loads custom CSS.

Author:
Sanket Kabariya
"""

import streamlit as st


class Theme:

    @staticmethod
    def load():

        with open(
            "assets/style.css",
            encoding="utf-8",
        ) as css:

            st.markdown(
                f"<style>{css.read()}</style>",
                unsafe_allow_html=True,
            )