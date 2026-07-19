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
    
if "upload_success" not in st.session_state:
    st.session_state.upload_success = False

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "table_name" not in st.session_state:
    st.session_state.table_name = ""

if "rows" not in st.session_state:
    st.session_state.rows = 0

if "columns" not in st.session_state:
    st.session_state.columns = 0

if "history" not in st.session_state:
    st.session_state.history = []