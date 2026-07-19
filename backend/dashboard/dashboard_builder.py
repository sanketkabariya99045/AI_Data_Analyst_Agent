"""
Dashboard Builder

Builds a complete dashboard by executing
multiple AI analysis requests.

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging
from typing import Callable

from backend.dashboard.dashboard_planner import (
    dashboard_planner,
)

logger = logging.getLogger(__name__)


class DashboardBuilder:
    """
    Builds complete dashboards.

    This class does NOT know anything
    about AgentManager.

    It only requires a callable that
    can process a question.
    """

    def build(
        self,
        *,
        dashboard_question: str,
        processor: Callable,
    ) -> dict:

        layout = dashboard_planner.plan(
            dashboard_question
        )

        dashboard = {

            "title": layout.title,

            "description": layout.description,

            "cards": [],

            "charts": [],

            "summary": None,

            "recommendations": [],

            "insights": [],
        }

        logger.info(
            "Building dashboard: %s",
            layout.title,
        )

        # ---------------------------------
        # Generate every chart
        # ---------------------------------

        for chart in layout.charts:

            logger.info(
                "Executing: %s",
                chart.question,
            )

            response = processor(

                question=chart.question,

            )

            dashboard["charts"].append({

                "title": chart.title,

                "question": chart.question,

                "response": response,

            })

        return dashboard


dashboard_builder = DashboardBuilder()