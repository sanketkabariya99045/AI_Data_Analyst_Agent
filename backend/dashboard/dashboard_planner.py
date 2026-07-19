"""
backend/dashboard/dashboard_planner.py

Enterprise Dashboard Planner.

Responsible for selecting the appropriate
dashboard template based on the user's request.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging

from backend.dashboard.dashboard_models import (
    DashboardPlan,
)
from backend.dashboard.dataset_classifier import (
    dataset_classifier,
)
from backend.dashboard.dashboard_templates import (
    dashboard_templates,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Dashboard Planner
# ==========================================================

class DashboardPlanner:
    """
    Enterprise Dashboard Planner.

    Responsibilities
    ----------------

    • Analyze dashboard request

    • Select dashboard template

    • Return DashboardPlan

    This class NEVER executes SQL.
    """

    # ------------------------------------------------------

    def plan(
        self,
        question: str,
    ) -> DashboardPlan:

        logger.info(
            "Planning dashboard..."
        )

        dataset_type = dataset_classifier.classify()

        logger.info(
            "Detected dataset type: %s",
            dataset_type,
        )

        # -----------------------------------
        # Sales
        # -----------------------------------

        if dataset_type == "sales":

            return dashboard_templates.sales_dashboard()

        # -----------------------------------
        # HR
        # -----------------------------------

        if dataset_type == "hr":

            return dashboard_templates.hr_dashboard()

        # -----------------------------------
        # Banking
        # -----------------------------------

        if dataset_type == "bank":

            return dashboard_templates.finance_dashboard()

        # -----------------------------------
        # Cricket
        # -----------------------------------

        if dataset_type == "cricket":

            return dashboard_templates.cricket_dashboard()

        # -----------------------------------
        # Generic
        # -----------------------------------

        return dashboard_templates.generic_dashboard()


# ==========================================================
# Singleton
# ==========================================================

dashboard_planner = DashboardPlanner()