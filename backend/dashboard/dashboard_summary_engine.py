"""
backend/dashboard/dashboard_summary_engine.py

Enterprise Dashboard Summary Engine.

Generates one executive dashboard summary
using all dashboard KPIs and charts.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging

from backend.dashboard.dashboard_models import (
    DashboardChart,
    DashboardKPI,
    DashboardSummary,
)

from backend.llm.llm_factory import (
    LLMFactory,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Dashboard Summary Engine
# ==========================================================

class DashboardSummaryEngine:
    """
    Enterprise Dashboard Summary Engine.

    Responsibilities
    ----------------

    • Build dashboard summary prompt

    • Call LLM once

    • Return DashboardSummary

    No SQL.

    No Charts.

    No KPIs.
    """

    def __init__(
        self,
        provider: str = "gemini",
    ):

        self._llm = LLMFactory.create(
            provider,
        )

    # ------------------------------------------------------

    def generate(

        self,

        *,

        title: str,

        kpis: list[DashboardKPI],

        charts: list[DashboardChart],

    ) -> DashboardSummary:

        logger.info(
            "Generating dashboard summary."
        )

        try:

            prompt = self._build_prompt(

                title,

                kpis,

                charts,

            )

            response = self._llm.generate(
                prompt,
            )

            return DashboardSummary(

                overview=response,

                recommendations=[],

                risks=[],

                opportunities=[],

            )

        except Exception as error:

            logger.exception(
                "Dashboard summary failed."
            )

            return DashboardSummary(

                overview=(
                    "Unable to generate "
                    "executive summary."
                ),

                recommendations=[],

                risks=[],

                opportunities=[],

            )

    # ------------------------------------------------------

    @staticmethod
    def _build_prompt(

        title: str,

        kpis: list[DashboardKPI],

        charts: list[DashboardChart],

    ) -> str:

        lines = [

            "You are an Executive Business Analyst.",

            "",

            f"Dashboard: {title}",

            "",

            "KPIs:",

        ]

        for kpi in kpis:

            lines.append(

                f"- {kpi.title}: {kpi.value}"

            )

        lines.append("")

        lines.append("Charts:")

        for chart in charts:

            lines.append(

                f"- {chart.title}"

            )

        lines.append("")

        lines.append(

            "Write a professional executive report."

        )

        lines.append(

            "Include:"

        )

        lines.append(

            "1. Executive Overview"

        )

        lines.append(

            "2. Key Findings"

        )

        lines.append(

            "3. Risks"

        )

        lines.append(

            "4. Opportunities"

        )

        lines.append(

            "5. Recommendations"

        )

        return "\n".join(lines)


# ==========================================================
# Singleton
# ==========================================================

dashboard_summary_engine = DashboardSummaryEngine()