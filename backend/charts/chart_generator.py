"""
Chart Generator

Coordinates chart selection, validation,
and Plotly chart creation.

Project:
AI Data Analyst
"""

from __future__ import annotations

from backend.charts.chart_models import (
    ChartRequest,
    ChartResult,
)

from backend.charts.chart_selector import chart_selector
from backend.charts.chart_validator import chart_validator
from backend.charts.plotly_service import plotly_service


class ChartGenerator:
    """
    Visualization orchestrator.
    """

    def generate(
        self,
        request: ChartRequest,
    ) -> ChartResult:
        """
        Generate a chart from a request.
        """

        try:

            # -----------------------------------
            # Step 1
            # Select chart
            # -----------------------------------

            config = chart_selector.select(request)

            # -----------------------------------
            # Step 2
            # Validate configuration
            # -----------------------------------

            validation = chart_validator.validate(
                request.dataframe,
                config,
            )

            if not validation.valid:

                return ChartResult(
                    success=False,
                    chart_type=config.chart_type,
                    figure=None,
                    config=config,
                    warnings=[],
                    error=validation.message,
                )

            # -----------------------------------
            # Step 3
            # Create figure
            # -----------------------------------

            figure = plotly_service.create_chart(
                request.dataframe,
                config,
            )

            # -----------------------------------
            # Step 4
            # Return
            # -----------------------------------

            return ChartResult(
                success=True,
                chart_type=config.chart_type,
                figure=figure,
                config=config,
                warnings=validation.warnings,
            )

        except Exception as error:

            return ChartResult(
                success=False,
                chart_type=request.preferred_chart,
                figure=None,
                config=None,
                warnings=[],
                error=str(error),
            )


chart_generator = ChartGenerator()