"""
Main Dashboard

Enterprise Dashboard Orchestrator

Author:
Sanket Kabariya
"""

from __future__ import annotations

import streamlit as st

from layout.dashboard_layout_v3 import (
    dashboard_layout_v3,
)

from components.upload_panel import UploadPanel
from components.dataset_info import DatasetInfo
from components.question_panel import QuestionPanel
from components.kpi_cards import KPICards
from components.chart_panel import ChartPanel
from components.summary_panel import SummaryPanel
from components.explanation_panel import ExplanationPanel
from components.sql_panel import SQLPanel
from components.result_table import ResultTable
from components.download_panel import DownloadPanel
from components.suggestion_panel import SuggestionPanel


class MainDashboard:

    def __init__(self):

        self.upload = UploadPanel()

        self.dataset = DatasetInfo()

        self.question = QuestionPanel()

        self.kpis = KPICards()

        self.chart = ChartPanel()

        self.summary = SummaryPanel()

        self.explanation = ExplanationPanel()

        self.sql = SQLPanel()

        self.table = ResultTable()

        self.download = DownloadPanel()

        self.suggestions = SuggestionPanel()

    # ==================================================

    def render(self):

        dashboard_layout_v3.header()

        self._landing()

        self._analysis()

    # ==================================================

    def _landing(self):

        left, right = dashboard_layout_v3.landing()

        with left:

            self.upload.render()

            st.divider()

            self.dataset.render()

        with right:

            self.question.render()

            st.divider()

            self.suggestions.render()

    # ==================================================

    def _analysis(self):

        if not st.session_state.get("generated_sql"):

            st.info(
                "👆 Upload a dataset and ask a business question."
            )

            return

        # ===============================
        # KPI Dashboard
        # ===============================

        self.kpis.render()

        st.divider()

        # ===============================
        # Chart + Summary
        # ===============================

        chart, summary = dashboard_layout_v3.analytics()

        with chart:

            self.chart.render()

        with summary:

            self.summary.render()

        st.divider()

        # ===============================
        # AI Explanation
        # ===============================

        self.explanation.render()

        st.divider()

        # ===============================
        # SQL + Result Table
        # ===============================

        sql, table = dashboard_layout_v3.workspace()

        with sql:

            self.sql.render()

        with table:

            self.table.render()

        st.divider()

        # ===============================
        # Downloads
        # ===============================

        self.download.render()