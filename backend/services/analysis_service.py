"""
backend/services/analysis_service.py

Enterprise Analysis Service

Central orchestration layer for the
Business Intelligence Engine.

Pipeline
--------
DataFrame
      │
      ├──────────┐
      ▼          ▼
InsightAgent  ChartAgent
      │          │
      └────┬─────┘
           ▼
AnalysisServiceResponse

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
import plotly.graph_objects as go

from backend.insights.insight_agent import (
    insight_agent,
)

from backend.charts.chart_agent import (
    chart_agent,
)

from backend.models.analysis_models import (
    AnalysisResult,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Response Model
# ==========================================================

@dataclass(slots=True)
class AnalysisServiceResponse:
    """
    Final response returned by the
    Analysis Service.
    """

    success: bool

    analysis: Optional[AnalysisResult]

    figure: Optional[go.Figure]

    chart_type: str

    warnings: list[str] = field(
        default_factory=list
    )

    error: Optional[str] = None


# ==========================================================
# Analysis Service
# ==========================================================

class AnalysisService:
    """
    Central orchestration service.

    Responsibilities
    ----------------

    • Execute business analysis

    • Generate visualization

    • Merge responses

    No SQL logic.

    No LLM logic.

    No Plotly implementation.
    """

    def analyze(
        self,
        *,
        dataframe: pd.DataFrame,
        question: str,
    ) -> AnalysisServiceResponse:

        logger.info(
            "Starting Analysis Service."
        )

        try:

            # ------------------------------------
            # Step 1
            # Generate business insights
            # ------------------------------------

            analysis = insight_agent.analyze(
                dataframe=dataframe,
                question=question,
            )

            logger.info(
                "Insight generation completed."
            )

            # ------------------------------------
            # Step 2
            # Generate visualization
            # ------------------------------------

            chart = chart_agent.generate(
                dataframe=dataframe,
                question=question,
            )

            if not chart.success:

                logger.warning(
                    "Visualization generation failed."
                )

                return AnalysisServiceResponse(
                    success=False,
                    analysis=analysis,
                    figure=None,
                    chart_type="",
                    warnings=chart.warnings,
                    error=chart.error,
                )

            #
            # Continue in Part 2
            #
            
                        # ------------------------------------
            # Step 3
            # Build final response
            # ------------------------------------

            logger.info(
                "Analysis Service completed successfully."
            )

            return AnalysisServiceResponse(
                success=True,
                analysis=analysis,
                figure=chart.figure,
                chart_type=chart.chart_type,
                warnings=chart.warnings,
                error=None,
            )

        except Exception as error:

            logger.exception(
                "Analysis Service failed."
            )

            return AnalysisServiceResponse(
                success=False,
                analysis=None,
                figure=None,
                chart_type="",
                warnings=[],
                error=str(error),
            )

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    @staticmethod
    def health_check() -> bool:
        """
        Health check used by API and
        integration tests.
        """

        return True


# ==========================================================
# Singleton
# ==========================================================

analysis_service = AnalysisService()