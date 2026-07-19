"""
backend/insights/recommendation_engine.py

Enterprise Recommendation Engine.

Generates business recommendations based on
trend and anomaly analysis.

Author: Sanket Kabariya
"""

from __future__ import annotations
import logging

from backend.models.analysis_models import (
    AnomalyResult,
    PriorityLevel,
    Recommendation,
    RecommendationResult,
    TrendDirection,
    TrendResult,
)
from backend.models.analysis_models import BusinessInsight
logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Enterprise Recommendation Engine.

    Converts business observations into actionable
    recommendations.

    Future versions can incorporate:
        • LLM recommendations
        • Forecast recommendations
        • KPI recommendations
        • Industry-specific business rules
    """

    def generate(
        self,
        trend: TrendResult,
        anomaly: AnomalyResult,
        insights: list | None = None,
    ) -> RecommendationResult:
        """
        Generate business recommendations.

        Parameters
        ----------
        trend : TrendResult

        anomaly : AnomalyResult

        Returns
        -------
        RecommendationResult
        """

        logger.info("Generating business recommendations.")

        recommendations: list[Recommendation] = []

        recommendations.extend(
            self._trend_recommendations(trend)
        )

        recommendations.extend(
            self._anomaly_recommendations(anomaly)
        )
        
        if insights is not None:
            recommendations.extend(
                self._business_recommendations(
                    insights
                )
            )

        logger.info(
            "%d recommendation(s) generated.",
            len(recommendations),
        )

        return RecommendationResult(
            total=len(recommendations),
            recommendations=recommendations,
        )

    # -----------------------------------------------------

    def _trend_recommendations(
        self,
        trend: TrendResult,
    ) -> list[Recommendation]:
        """
        Generate trend-based recommendations.
        """

        if trend.trend == TrendDirection.INCREASING:

            return [
                Recommendation(
                    priority=PriorityLevel.MEDIUM,
                    category="Growth",
                    recommendation=(
                        "Business demand is increasing. "
                        "Consider scaling inventory, "
                        "production capacity, and staffing."
                    ),
                )
            ]

        if trend.trend == TrendDirection.DECREASING:

            return [
                Recommendation(
                    priority=PriorityLevel.HIGH,
                    category="Revenue",
                    recommendation=(
                        "Business performance is declining. "
                        "Review pricing strategy, marketing "
                        "campaigns, and customer retention."
                    ),
                )
            ]

        return [
            Recommendation(
                priority=PriorityLevel.LOW,
                category="Monitoring",
                recommendation=(
                    "Business performance is stable. "
                    "Continue monitoring key performance "
                    "indicators."
                ),
            )
        ]


    def _business_recommendations(
        self,
        insights,
    ) -> list[Recommendation]:
        """
        Generate recommendations from business insights.
        """

        recommendations: list[Recommendation] = []

        for insight in insights:

            title = insight.title.lower()

            # Revenue
            if "revenue" in title:

                recommendations.append(

                    Recommendation(

                        priority=PriorityLevel.MEDIUM,

                        category="Revenue",

                        recommendation=(
                            "Continue investing in high-performing "
                            "revenue sources while monitoring "
                            "future growth."
                        ),
                    )

                )

            # Profit

            elif "profit" in title:

                recommendations.append(

                    Recommendation(

                        priority=PriorityLevel.HIGH,

                        category="Profit",

                        recommendation=(
                            "Review cost structure and improve "
                            "profit margins through pricing or "
                            "operational efficiency."
                        ),
                    )

                )

            # Region

            elif "region" in title:

                recommendations.append(

                    Recommendation(

                        priority=PriorityLevel.MEDIUM,

                        category="Market",

                        recommendation=(
                            "Focus marketing investment on "
                            "high-performing regions while "
                            "improving weaker markets."
                        ),
                    )

                )

            # Discount

            elif "discount" in title:

                recommendations.append(

                    Recommendation(

                        priority=PriorityLevel.LOW,

                        category="Pricing",

                        recommendation=(
                            "Review discount strategy regularly "
                            "to ensure profitability is maintained."
                        ),
                    )

                )

        return recommendations
    # -----------------------------------------------------

    def _anomaly_recommendations(
        self,
        anomaly: AnomalyResult,
    ) -> list[Recommendation]:
        """
        Generate anomaly-based recommendations.
        """

        if anomaly.anomaly_count > 0:

            return [
                Recommendation(
                    priority=PriorityLevel.HIGH,
                    category="Risk",
                    recommendation=(
                        f"{anomaly.anomaly_count} statistical "
                        "anomaly(s) detected. Investigate "
                        "unusual transactions, operational "
                        "events, or potential data quality "
                        "issues."
                    ),
                )
            ]

        return [
            Recommendation(
                priority=PriorityLevel.LOW,
                category="Data Quality",
                recommendation=(
                    "No significant anomalies detected. "
                    "Current dataset appears statistically "
                    "consistent."
                ),
            )
        ]


recommendation_engine = RecommendationEngine()