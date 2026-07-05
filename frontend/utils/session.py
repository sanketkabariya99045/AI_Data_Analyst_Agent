import streamlit as st


def initialize_session():
    defaults = {
    "uploaded": False,
    "table_name": None,
    "rows": None,
    "columns": None,
    "question": "",
    "generated_sql": "",
    "summary": "",
    "report": {},
    "chart": None,
    "query_result": None,
}

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_analysis():
    st.session_state.generated_sql = ""
    st.session_state.summary = ""
    st.session_state.report = {}
    st.session_state.chart = None
    st.session_state.query_result = None