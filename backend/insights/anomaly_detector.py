"""
backend/insights/anomaly_detector.py

Enterprise Anomaly Detection Engine.

Detects statistical anomalies using Z-score analysis.

Author: Sanket Kabariya
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from backend.models.analysis_models import (
    Anomaly,
    AnomalyResult,
)

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    Enterprise anomaly detection engine.

    Uses statistical Z-score analysis to identify
    unusual observations inside business datasets.
    """

    DEFAULT_THRESHOLD = 3.0

    def detect(
        self,
        dataframe: pd.DataFrame,
        value_column: str,
        threshold: float = DEFAULT_THRESHOLD,
    ) -> AnomalyResult:
        """
        Detect anomalies using Z-score.

        Parameters
        ----------
        dataframe : pd.DataFrame

        value_column : str

        threshold : float

        Returns
        -------
        AnomalyResult
        """

        logger.info(
            "Starting anomaly detection for column '%s'.",
            value_column,
        )

        self._validate_dataframe(
            dataframe,
            value_column,
        )

        values = dataframe[value_column].astype(float)

        mean = values.mean()

        std = values.std()

        if std == 0:

            logger.info(
                "Column has zero variance."
            )

            return AnomalyResult(
                total_rows=len(dataframe),
                anomaly_count=0,
                anomalies=[],
                message="No anomalies detected (zero variance).",
            )

        z_scores = self._calculate_z_scores(
            values,
            mean,
            std,
        )

        anomalies = self._extract_anomalies(
            values,
            z_scores,
            threshold,
        )

        if anomalies:

            message = (
                f"{len(anomalies)} anomaly(s) detected."
            )

        else:

            message = "No anomalies detected."

        logger.info(
            "Anomaly detection completed successfully."
        )

        return AnomalyResult(
            total_rows=len(dataframe),
            anomaly_count=len(anomalies),
            anomalies=anomalies,
            message=message,
        )

    # -----------------------------------------------------

    def has_anomalies(
        self,
        dataframe: pd.DataFrame,
        value_column: str,
    ) -> bool:
        """
        Convenience helper.
        """

        result = self.detect(
            dataframe,
            value_column,
        )

        return result.anomaly_count > 0

    # -----------------------------------------------------

    @staticmethod
    def _calculate_z_scores(
        values: pd.Series,
        mean: float,
        std: float,
    ) -> np.ndarray:
        """
        Calculate Z-scores.
        """

        return (values - mean) / std

    # -----------------------------------------------------

    @staticmethod
    def _extract_anomalies(
        values: pd.Series,
        z_scores: np.ndarray,
        threshold: float,
    ) -> list[Anomaly]:
        """
        Extract anomaly objects.
        """

        anomalies: list[Anomaly] = []

        for index, score in enumerate(z_scores):

            if abs(score) >= threshold:

                anomalies.append(
                    Anomaly(
                        index=index,
                        value=float(values.iloc[index]),
                        z_score=round(
                            float(score),
                            2,
                        ),
                    )
                )

        return anomalies

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

        if dataframe[value_column].dropna().empty:
            raise ValueError(
                "Selected column contains no values."
            )


anomaly_detector = AnomalyDetector()