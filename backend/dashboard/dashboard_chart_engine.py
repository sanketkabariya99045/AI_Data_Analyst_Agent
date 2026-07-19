"""
backend/dashboard/dashboard_chart_engine.py

Enterprise Dashboard Chart Engine.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging

from backend.charts.chart_agent import chart_agent
from backend.dashboard.dashboard_models import DashboardChart
from backend.services.sql_execution_service import (
    SQLExecutionResponse,
)

logger = logging.getLogger(__name__)


class DashboardChartEngine:
    """
    Builds dashboard charts from SQL results.
    """

    def build(
        self,
        results: list[SQLExecutionResponse],
    ) -> list[DashboardChart]:

        logger.info("Building dashboard charts...")

        charts: list[DashboardChart] = []

        for result in results:

            # Skip failed SQL
            if not result.success:
                continue

            if result.dataframe is None:
                continue

            if result.dataframe.empty:
                continue

            # Need at least 2 columns for a chart
            if result.dataframe.shape[1] < 2:
                logger.warning(
                    "Skipping chart '%s' because dataframe has less than 2 columns.",
                    result.question,
                )
                continue

            try:

                chart = chart_agent.generate(

                    dataframe=result.dataframe,

                    question=result.question,

                )

                if not chart.success:
                    logger.warning(
                        "Chart generation failed for %s",
                        result.question,
                    )
                    continue

                charts.append(

                    DashboardChart(

                        title=result.question,

                        figure=chart.figure,

                        chart_type=str(chart.chart_type),

                        success=True,

                    )

                )

            except Exception:

                logger.exception(
                    "Chart generation failed."
                )

        logger.info(
            "Generated %d dashboard charts.",
            len(charts),
        )

        return charts


dashboard_chart_engine = DashboardChartEngine()