"""
backend/insights/trend_detector.py

Enterprise Trend Detection Engine.

Detects business trends from analytical datasets.

Author: Sanket Kabariya
"""

from __future__ import annotations

import logging

import pandas as pd

from backend.models.analysis_models import (
    TrendDirection,
    TrendResult,
)

logger = logging.getLogger(__name__)


class TrendDetector:
    """
    Detects business trends from numeric data.

    This detector is responsible for determining whether
    a metric is increasing, decreasing, or stable.

    It serves as the foundation for:
        • Insight Engine
        • Forecast Engine
        • Dashboard Engine
    """

    STABLE_THRESHOLD = 5.0

    def detect(
        self,
        dataframe: pd.DataFrame,
        value_column: str,
    ) -> TrendResult:
        """
        Detect trend from a numeric column.

        If trend detection is not possible (for example,
        only one value is available), return a neutral
        TrendResult instead of raising an exception.
        """

        logger.info(
            "Starting trend detection for column '%s'.",
            value_column,
        )

        # -------------------------------------------------
        # Basic validation
        # -------------------------------------------------

        if dataframe.empty:

            logger.warning(
                "Trend detection skipped: empty dataframe."
            )

            return TrendResult(
                trend=TrendDirection.STABLE,
                percentage_change=0.0,
                first_value=0.0,
                last_value=0.0,
                message="Trend analysis skipped because the dataset is empty.",
            )

        if value_column not in dataframe.columns:

            logger.warning(
                "Trend detection skipped: column '%s' not found.",
                value_column,
            )

            return TrendResult(
                trend=TrendDirection.STABLE,
                percentage_change=0.0,
                first_value=0.0,
                last_value=0.0,
                message=f"Trend analysis skipped because '{value_column}' does not exist.",
            )

        values = dataframe[value_column].dropna()

        # -------------------------------------------------
        # Not enough values
        # -------------------------------------------------

        if len(values) < 2:

            value = float(values.iloc[0]) if len(values) == 1 else 0.0

            logger.info(
                "Trend detection skipped: only %d value(s).",
                len(values),
            )

            return TrendResult(
                trend=TrendDirection.STABLE,
                percentage_change=0.0,
                first_value=value,
                last_value=value,
                message="Trend analysis is not available because only one data point was returned.",
            )

        # -------------------------------------------------
        # Normal trend detection
        # -------------------------------------------------

        first_value = float(values.iloc[0])

        last_value = float(values.iloc[-1])

        percentage_change = self._calculate_percentage_change(
            first_value,
            last_value,
        )

        direction = self._determine_direction(
            percentage_change,
        )

        message = (
            f"{direction.value} trend detected "
            f"({percentage_change:.2f}% change)."
        )

        logger.info(
            "Trend detection completed successfully."
        )

        return TrendResult(
            trend=direction,
            percentage_change=round(
                percentage_change,
                2,
            ),
            first_value=first_value,
            last_value=last_value,
            message=message,
        )

    # -----------------------------------------------------

    def top_growth(
        self,
        dataframe: pd.DataFrame,
        value_column: str,
        n: int = 5,
    ) -> pd.DataFrame:
        """
        Return highest values.
        """

        self._validate_dataframe(
            dataframe,
            value_column,
        )

        return dataframe.nlargest(
            n,
            value_column,
        )

    # -----------------------------------------------------

    def top_decline(
        self,
        dataframe: pd.DataFrame,
        value_column: str,
        n: int = 5,
    ) -> pd.DataFrame:
        """
        Return lowest values.
        """

        self._validate_dataframe(
            dataframe,
            value_column,
        )

        return dataframe.nsmallest(
            n,
            value_column,
        )

    # -----------------------------------------------------

    @staticmethod
    def _calculate_percentage_change(
        first: float,
        last: float,
    ) -> float:
        """
        Calculate percentage change.
        """

        if first == 0:
            return 0.0

        return ((last - first) / first) * 100

    # -----------------------------------------------------

    def _determine_direction(
        self,
        percentage: float,
    ) -> TrendDirection:
        """
        Determine trend direction.
        """

        if percentage > self.STABLE_THRESHOLD:
            return TrendDirection.INCREASING

        if percentage < -self.STABLE_THRESHOLD:
            return TrendDirection.DECREASING

        return TrendDirection.STABLE

    # -----------------------------------------------------

    @staticmethod
    def _validate_dataframe(
        dataframe: pd.DataFrame,
        value_column: str,
    ) -> None:
        """
        Validate analysis input.
        """

        if dataframe.empty:
            raise ValueError(
                "Cannot analyze an empty DataFrame."
            )

        if value_column not in dataframe.columns:
            raise ValueError(
                f"Column '{value_column}' does not exist."
            )


trend_detector = TrendDetector()