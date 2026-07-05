"""
Chart Validator

Validates chart configuration before
creating Plotly figures.

Project:
AI Data Analyst
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import pandas as pd

from backend.charts.chart_models import ChartConfig, ChartType


@dataclass
class ValidationResult:
    """
    Chart validation result.
    """

    valid: bool

    message: str

    warnings: List[str] = field(default_factory=list)


class ChartValidator:
    """
    Validates chart configurations.
    """

    def validate(
        self,
        dataframe: pd.DataFrame,
        config: ChartConfig,
    ) -> ValidationResult:

        warnings = []

        # -------------------------------------
        # Empty DataFrame
        # -------------------------------------

        if dataframe.empty:

            return ValidationResult(
                valid=False,
                message="The dataset is empty."
            )

        # -------------------------------------
        # Validate X Axis
        # -------------------------------------

        if config.x_axis not in dataframe.columns:

            return ValidationResult(
                valid=False,
                message=f"Column '{config.x_axis}' does not exist."
            )

        # -------------------------------------
        # Validate Y Axis
        # -------------------------------------

        if (
            config.y_axis
            and config.y_axis not in dataframe.columns
        ):

            return ValidationResult(
                valid=False,
                message=f"Column '{config.y_axis}' does not exist."
            )

        # -------------------------------------
        # Numeric Validation
        # -------------------------------------

        numeric_required = {

            ChartType.BAR,

            ChartType.LINE,

            ChartType.SCATTER,

            ChartType.AREA,

            ChartType.BOX,

            ChartType.PIE,
        }

        if (
            config.chart_type in numeric_required
            and config.y_axis
        ):

            if not pd.api.types.is_numeric_dtype(
                dataframe[config.y_axis]
            ):

                return ValidationResult(
                    valid=False,
                    message=(
                        f"'{config.y_axis}' "
                        "must be numeric."
                    )
                )

        # -------------------------------------
        # Histogram
        # -------------------------------------

        if config.chart_type == ChartType.HISTOGRAM:

            if not pd.api.types.is_numeric_dtype(
                dataframe[config.x_axis]
            ):

                return ValidationResult(
                    valid=False,
                    message=(
                        "Histogram requires "
                        "a numeric column."
                    )
                )

        # -------------------------------------
        # Heatmap
        # -------------------------------------

        if config.chart_type == ChartType.HEATMAP:

            numeric = dataframe.select_dtypes(
                include="number"
            )

            if numeric.shape[1] < 2:

                return ValidationResult(
                    valid=False,
                    message=(
                        "Heatmap requires "
                        "at least two numeric columns."
                    )
                )

        # -------------------------------------
        # Warnings
        # -------------------------------------

        if len(dataframe) > 100000:

            warnings.append(
                "Large dataset detected. "
                "Rendering may be slower."
            )

        if dataframe.isnull().sum().sum() > 0:

            warnings.append(
                "Dataset contains missing values."
            )

        if dataframe.duplicated().sum() > 0:

            warnings.append(
                "Dataset contains duplicate rows."
            )

        return ValidationResult(

            valid=True,

            message="Validation successful.",

            warnings=warnings,
        )


chart_validator = ChartValidator()