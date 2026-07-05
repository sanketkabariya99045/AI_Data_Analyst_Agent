"""
backend/insights/explanation_agent.py

Enterprise Explanation Agent.

Responsible for converting structured business
analysis into professional executive reports.

Business logic should never exist here.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging

from backend.llm.llm_factory import LLMFactory

from backend.models.analysis_models import (
    AnalysisMetadata,
    AnomalyResult,
    ExplanationResult,
    RecommendationResult,
    SummaryResult,
    TrendResult,
)

from backend.prompts.insight_prompt import (
    InsightPromptBuilder,
)

logger = logging.getLogger(__name__)


class ExplanationAgent:
    """
    Enterprise Explanation Agent.

    Responsibilities
    ----------------

    • Build LLM prompts

    • Call the configured LLM

    • Return ExplanationResult

    No business analytics should exist here.
    """

    def __init__(
        self,
        provider: str = "gemini",
    ) -> None:

        self._llm = LLMFactory.create(provider)

    # ---------------------------------------------------------

    @property
    def model_name(self) -> str:
        """
        Current LLM model.
        """

        return getattr(
            self._llm,
            "model_name",
            "Unknown",
        )

    # ---------------------------------------------------------

    def generate(
        self,
        *,
        metadata: AnalysisMetadata,
        trend: TrendResult,
        anomaly: AnomalyResult,
        recommendation: RecommendationResult,
        summary: SummaryResult,
    ) -> ExplanationResult:
        """
        Generate the executive report.
        """

        logger.info(
            "Generating executive explanation."
        )

        try:

            prompt = (
                InsightPromptBuilder
                .build_explanation_prompt(
                    metadata=metadata,
                    trend=trend,
                    anomaly=anomaly,
                    recommendation=recommendation,
                    summary=summary,
                )
            )

            response = self._llm.generate(
                prompt
            )

            logger.info(
                "Executive report generated."
            )

            return ExplanationResult(
                success=True,
                overview=response,
                trends=trend.message,
                risks=(
                    "No significant business risks detected."
                    if anomaly.anomaly_count == 0
                    else f"{anomaly.anomaly_count} potential anomalies detected that should be reviewed."
                ),
                opportunities=(
                    "Review the identified trends and recommendations for potential business improvements."
                ),
                recommendations="\n".join(
                    [
                        r.recommendation
                        for r in recommendation.recommendations
                    ]
                ) or "No recommendations available.",
                conclusion=response,
                model=self.model_name,
                error=None,
            )

        except Exception as exc:

            logger.exception(
                "Explanation generation failed."
            )

            return ExplanationResult(
                success=False,
                overview="",
                trends="",
                risks="",
                opportunities="",
                recommendations="",
                conclusion="",
                model=self.model_name,
                error=str(exc),
            )


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

explanation_agent = ExplanationAgent()