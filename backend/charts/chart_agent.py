"""
backend/charts/chart_agent.py

Enterprise Chart Agent.

Responsible only for visualization generation.

Pipeline
--------
DataFrame
    ↓
ChartGenerator
    ↓
ChartAgentResponse

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
import plotly.graph_objects as go

from backend.charts.chart_generator import chart_generator
from backend.charts.chart_models import ChartRequest

logger = logging.getLogger(__name__)


# =====================================================
# Response Model
# =====================================================

@dataclass(slots=True)
class ChartAgentResponse:
    """
    Final response returned by Chart Agent.
    """

    success: bool

    figure: Optional[go.Figure]

    chart_type: str

    warnings: list[str] = field(
        default_factory=list
    )

    error: Optional[str] = None


# =====================================================
# Chart Agent
# =====================================================

class ChartAgent:
    """
    Enterprise Visualization Agent.

    Responsibilities
    ----------------

    • Build ChartRequest

    • Generate Plotly figure

    • Return ChartAgentResponse

    No AI logic.

    No business analysis.

    No LLM calls.
    """

    def generate(
        self,
        *,
        question: str,
        dataframe: pd.DataFrame,
    ) -> ChartAgentResponse:
        """
        Generate visualization.
        """

        logger.info(
            "Starting visualization generation."
        )

        try:

            # ----------------------------------
            # Build request
            # ----------------------------------

            request = ChartRequest(
                question=question,
                dataframe=dataframe,
            )

            # ----------------------------------
            # Generate chart
            # ----------------------------------

            result = chart_generator.generate(
                request
            )

            if not result.success:

                logger.error(
                    "Chart generation failed."
                )

                return ChartAgentResponse(
                    success=False,
                    figure=None,
                    chart_type="",
                    warnings=[],
                    error=result.error,
                )
                
                logger.info(
                "Visualization generated successfully."
            )

            return ChartAgentResponse(
                success=True,
                figure=result.figure,
                chart_type=result.chart_type.value,
                warnings=result.warnings,
                error=None,
            )

        except Exception as error:

            logger.exception(
                "Unexpected error during chart generation."
            )

            return ChartAgentResponse(
                success=False,
                figure=None,
                chart_type="",
                warnings=[],
                error=str(error),
            )


# =====================================================
# Singleton
# =====================================================

chart_agent = ChartAgent()