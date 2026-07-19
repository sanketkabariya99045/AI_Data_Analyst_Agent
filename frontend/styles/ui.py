import streamlit as st


def section(title: str):

    st.markdown(f"## {title}")


def divider():

    st.markdown("<br>", unsafe_allow_html=True)