"""
backend/insights/insight_agent.py

Enterprise Insight Agent

Coordinates the complete Business Intelligence
analysis pipeline.

Pipeline
--------
DataFrame
    ↓
Column Selector
    ↓
Trend Detector
    ↓
Anomaly Detector
    ↓
Recommendation Engine
    ↓
Summary Generator
    ↓
Explanation Agent
    ↓
AnalysisResult

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging
import time

import pandas as pd

from backend.insights.column_selector import (
    ColumnSelector,
)
from backend.insights.trend_detector import (
    TrendDetector,
)
from backend.insights.anomaly_detector import (
    AnomalyDetector,
)
from backend.insights.recommendation_engine import (
    RecommendationEngine,
)
from backend.insights.summary_generator import (
    SummaryGenerator,
)
from backend.insights.explanation_agent import (
    ExplanationAgent,
)

from backend.models.analysis_models import (
    AnalysisMetadata,
    AnalysisResult,
)

logger = logging.getLogger(__name__)


class InsightAgent:
    """
    Enterprise Business Intelligence Agent.

    Responsible only for orchestration.

    Individual business logic is delegated to:

    • ColumnSelector
    • TrendDetector
    • AnomalyDetector
    • RecommendationEngine
    • SummaryGenerator
    • ExplanationAgent
    """

    def __init__(
        self,
        *,
        column_selector: ColumnSelector | None = None,
        trend_detector: TrendDetector | None = None,
        anomaly_detector: AnomalyDetector | None = None,
        recommendation_engine: RecommendationEngine | None = None,
        summary_generator: SummaryGenerator | None = None,
        explanation_agent: ExplanationAgent | None = None,
    ) -> None:

        self.column_selector = (
            column_selector
            or ColumnSelector()
        )

        self.trend_detector = (
            trend_detector
            or TrendDetector()
        )

        self.anomaly_detector = (
            anomaly_detector
            or AnomalyDetector()
        )

        self.recommendation_engine = (
            recommendation_engine
            or RecommendationEngine()
        )

        self.summary_generator = (
            summary_generator
            or SummaryGenerator()
        )

        self.explanation_agent = (
            explanation_agent
            or ExplanationAgent()
        )

    # =====================================================
    # PUBLIC API
    # =====================================================

    def analyze(
        self,
        dataframe: pd.DataFrame,
        question: str,
    ) -> AnalysisResult:
        """
        Execute the Business Intelligence pipeline.
        """

        logger.info(
            "Starting Business Intelligence analysis."
        )

        start_time = time.perf_counter()

        self._validate_dataframe(
            dataframe,
        )

        # -------------------------------------------------
        # Automatic Column Selection
        # -------------------------------------------------

        selected = self.column_selector.select(
            dataframe
        )

        if selected.metric is None:

            raise ValueError(
                "No numeric metric column detected."
            )

        logger.info(
            "Selected metric column: %s",
            selected.metric,
        )

        # -------------------------------------------------
        # Trend Detection
        # -------------------------------------------------

        trend = self.trend_detector.detect(
            dataframe=dataframe,
            value_column=selected.metric,
        )

        logger.info(
            "Trend detected: %s",
            trend.trend.value,
        )

        # -------------------------------------------------
        # Anomaly Detection
        # -------------------------------------------------

        anomaly = self.anomaly_detector.detect(
            dataframe=dataframe,
            value_column=selected.metric,
        )

        logger.info(
            "%d anomaly(s) detected.",
            anomaly.anomaly_count,
        )

        # -------------------------------------------------
        # Recommendation Generation
        # -------------------------------------------------

        recommendations = (
            self.recommendation_engine.generate(
                trend=trend,
                anomaly=anomaly,
            )
        )

        logger.info(
            "%d recommendation(s) generated.",
            recommendations.total,
        )

        #
        # Continue in Response 2
        #
        
        # -------------------------------------------------
        # Executive Summary
        # -------------------------------------------------

        summary = (
            self.summary_generator.generate(
                trend=trend,
                anomaly=anomaly,
                recommendations=recommendations,
            )
        )

        logger.info(
            "Executive summary generated."
        )

        # -------------------------------------------------
        # Analysis Metadata
        # -------------------------------------------------

        metadata = AnalysisMetadata(
            question=question,

            total_rows=len(dataframe),

            total_columns=len(
                dataframe.columns
            ),

            execution_time=round(
                time.perf_counter() - start_time,
                4,
            ),

            selected_metric=selected.metric,

            selected_category=selected.category,

            selected_datetime=selected.datetime,
        )

        logger.info(
            "Analysis metadata created."
        )

        # -------------------------------------------------
        # AI Business Explanation
        # -------------------------------------------------


        try:

            explanation = (
                self.explanation_agent.generate(
                    metadata=metadata,
                    trend=trend,
                    anomaly=anomaly,
                    recommendation=recommendations,
                    summary=summary,
                )
            )

            logger.info(
                "Executive explanation generated."
            )

        except Exception as error:

            logger.warning(
                "LLM explanation skipped: %s",
                error,
            )

            from backend.models.analysis_models import (
                ExplanationResult,
            )

            explanation = ExplanationResult(
                success=False,
                overview="AI explanation unavailable.",
                trends="",
                risks="",
                opportunities="",
                recommendations="",
                conclusion="",
                model="Gemini",
                error=str(error),
            )

        # -------------------------------------------------
        # Final Analysis Result
        # -------------------------------------------------

        analysis = AnalysisResult(

            metadata=metadata,

            summary=summary,

            explanation=explanation,

            trends=[
                trend,
            ],

            anomalies=[
                anomaly,
            ],

            recommendations=[
                recommendations,
            ],

            kpis=[],

            insights=[],

            charts=[],

            statistics=[],
        )

        logger.info(
            "Business analysis completed successfully."
        )

        return analysis

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    @staticmethod
    def _validate_dataframe(
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate dataframe before analysis.
        """

        if dataframe is None:
            raise ValueError(
                "DataFrame cannot be None."
            )

        if dataframe.empty:
            raise ValueError(
                "Cannot analyze an empty DataFrame."
            )

        if len(dataframe.columns) == 0:
            raise ValueError(
                "DataFrame contains no columns."
            )

    # -----------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Health check used by API
        and integration tests.
        """

        return True


# =========================================================
# Singleton
# =========================================================

insight_agent = InsightAgent()