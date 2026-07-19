"""
backend/insights/summary_generator.py

Enterprise Summary Generator.

Creates a structured executive summary from
trend analysis, anomaly detection, and
business recommendations.

Author: Sanket Kabariya
"""

from __future__ import annotations

import logging

from backend.models.analysis_models import (
    AnomalyResult,
    RecommendationResult,
    SummaryResult,
    TrendDirection,
    TrendResult,
)

logger = logging.getLogger(__name__)


class SummaryGenerator:
    """
    Enterprise Executive Summary Generator.

    Generates structured summaries that can be
    consumed by:

    • Explanation Agent
    • Dashboard Generator
    • Report Generator
    • Forecast Engine
    """

    def generate(
        self,
        trend: TrendResult,
        anomaly: AnomalyResult,
        recommendations: RecommendationResult,
    ) -> SummaryResult:
        """
        Generate executive summary.
        """

        logger.info("Generating executive summary.")

        overview = self._build_overview(trend)

        trend_summary = trend.message

        anomaly_summary = anomaly.message

        recommendation_summary = [
            recommendation.recommendation
            for recommendation in recommendations.recommendations
        ]

        # -------------------------------------------------
        # Executive Summary
        # -------------------------------------------------

        executive_summary = (
            f"{overview} "
            f"{trend_summary} "
            f"{anomaly_summary}"
        )

        if recommendation_summary:

            executive_summary += (
                " Key recommendations: "
                + ", ".join(recommendation_summary)
                + "."
            )

        logger.info(
            "Executive summary generated successfully."
        )

        return SummaryResult(
            executive_summary=executive_summary,
            overview=overview,
            trend_summary=trend_summary,
            anomaly_summary=anomaly_summary,
            recommendation_summary=recommendation_summary,
        )
        
        # -----------------------------------------------------

    def generate_empty_summary(
        self,
    ) -> SummaryResult:
        """
        Summary used when the SQL query returns
        zero rows.
        """

        return SummaryResult(

            executive_summary=(
                "The query executed successfully, "
                "but no matching records were found."
            ),

            overview=(
                "No data matched the requested "
                "criteria."
            ),

            trend_summary=(
                "Trend analysis is unavailable."
            ),

            anomaly_summary=(
                "No anomalies detected because "
                "the result set is empty."
            ),

            recommendation_summary=[
                "Try broadening your filters.",
                "Verify the requested conditions.",
            ],
        )
    # -----------------------------------------------------

    @staticmethod
    def _build_overview(
        trend: TrendResult,
    ) -> str:
        """
        Build executive overview based on trend.
        """

        if trend.trend == TrendDirection.INCREASING:

            return (
                "Overall business performance shows "
                "positive growth with an upward trend "
                "in the selected business metric."
            )

        if trend.trend == TrendDirection.DECREASING:

            return (
                "Business performance indicates a "
                "declining trend that requires "
                "management attention."
            )

        return (
            "Business performance remains stable "
            "with no significant upward or downward "
            "movement."
        )

    # -----------------------------------------------------

    def key_findings(
        self,
        trend: TrendResult,
        anomaly: AnomalyResult,
    ) -> list[str]:
        """
        Generate structured key findings.

        This method will be used later by
        Dashboard Generator and Forecast Engine.
        """

        findings: list[str] = []

        findings.append(trend.message)

        findings.append(anomaly.message)

        if anomaly.anomaly_count > 0:

            findings.append(
                "Unusual observations were detected "
                "that should be investigated."
            )

        else:

            findings.append(
                "Dataset appears statistically "
                "consistent."
            )

        return findings


summary_generator = SummaryGenerator()