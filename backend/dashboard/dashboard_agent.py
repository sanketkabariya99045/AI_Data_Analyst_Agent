"""
backend/dashboard/dashboard_agent.py

Enterprise Dashboard Agent.

Public entry point for AI Dashboard generation.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging



from backend.dashboard.dashboard_models import (
    DashboardResult,
)

from backend.dashboard.dashboard_planner import (
    dashboard_planner,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Dashboard Agent
# ==========================================================

class DashboardAgent:
    """
    Enterprise Dashboard Agent.

    Responsibilities
    ----------------

    • Receive dashboard request

    • Generate DashboardPlan

    • Execute DashboardPlan

    • Return DashboardResult

    Contains NO SQL logic.
    """

    # ------------------------------------------------------

    def generate_dashboard(
        self,
        question: str,
    ) -> DashboardResult:

        logger.info(
            "Generating dashboard for request: %s",
            question,
        )

        try:

            # --------------------------------------------
            # Build dashboard plan
            # --------------------------------------------

            plan = dashboard_planner.plan(
                question
            )

            logger.info(
                "Dashboard plan created with %d widgets.",
                len(plan.widgets),
            )

            # --------------------------------------------
            # Execute dashboard
            # --------------------------------------------

            result = dashboard_executor.execute(
                plan
            )

            logger.info(
                "Dashboard generated successfully."
            )

            return result

        except Exception as error:

            logger.exception(
                "Dashboard generation failed."
            )

            return DashboardResult(

                success=False,

                title="Dashboard Generation Failed",

                description="",

                widgets=[],

                metadata={},

                error=str(error),

            )


# ==========================================================
# Singleton
# ==========================================================

dashboard_agent = DashboardAgent()