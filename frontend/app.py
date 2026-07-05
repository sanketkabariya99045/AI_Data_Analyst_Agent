import streamlit as st

from utils.session import initialize_session

from components.sidebar import SidebarComponent
from components.question_box import QuestionBox
from components.sql_viewer import SQLViewer
from components.summary_view import SummaryView
from components.report_view import ReportView
from components.chart_view import ChartView

from components.upload_panel import UploadPanel
upload_panel = UploadPanel()
upload_panel.render()

from components.question_panel import QuestionPanel
question_panel = QuestionPanel()
question_panel.render()

from components.sql_panel import SQLPanel
sql_panel = SQLPanel()
sql_panel.render()

from components.result_table import ResultTable
result_table = ResultTable()
result_table.render()

from components.kpi_cards import KPICards
kpi_cards = KPICards()
kpi_cards.render()

from components.summary_panel import SummaryPanel
summary_panel = SummaryPanel()
summary_panel.render()

from components.explanation_panel import ExplanationPanel
explanation_panel = ExplanationPanel()
explanation_panel.render()

from components.chart_panel import ChartPanel
chart_panel = ChartPanel()
chart_panel.render()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Initialize Session
# --------------------------------------------------

initialize_session()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

SidebarComponent.render()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 AI Data Analyst Platform")

st.markdown(
    """
Ask questions about your uploaded dataset using natural language.
The AI will automatically generate SQL, execute it, analyze the results,
and produce business insights with interactive visualizations.
"""
)

st.divider()


# --------------------------------------------------
# Question Section
# --------------------------------------------------

QuestionBox.render()

st.divider()


# --------------------------------------------------
# Analysis Results
# --------------------------------------------------

if st.session_state.generated_sql:

    left_col, right_col = st.columns([1, 1])

    with left_col:
        SQLViewer.render()

    with right_col:
        SummaryView.render()

    st.divider()

    ReportView.render()

    st.divider()

    ChartView.render()

else:

    st.info(
        "Upload a dataset and ask a question to begin your analysis."
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "AI Data Analyst Platform • FastAPI • DuckDB • Gemini • Plotly • Streamlit"
)