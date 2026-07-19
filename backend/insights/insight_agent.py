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
from backend.intelligence.insight_generator import (
    insight_generator,
)

from backend.intelligence.column_detector import (
    column_detector,
)

from backend.intelligence.statistic_generator import (
    statistic_generator,
)

from backend.intelligence.narrative_generator import (
    narrative_generator,
)

from backend.models.analysis_models import (
    ExplanationResult,
)

from backend.insights.kpi_generator import kpi_generator
from backend.models.analysis_models import BusinessInsight


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

        self.kpi_generator = kpi_generator
        self.insight_generator = insight_generator
        self.statistic_generator = statistic_generator
        self.narrative_generator = narrative_generator

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

        if not self._validate_dataframe(dataframe):

            logger.info(
                "Query returned no rows."
            )

            empty_metadata = AnalysisMetadata(
                question=question,
                total_rows=0,
                total_columns=len(dataframe.columns),
                execution_time=round(
                    time.perf_counter() - start_time,
                    4,
                ),
            )

            empty_summary = self.summary_generator.generate_empty_summary()

            empty_explanation = ExplanationResult(
                success=True,
                overview="The query executed successfully but returned no rows.",
                trends="No trends available.",
                risks="None.",
                opportunities="Try a broader query.",
                recommendations="Modify the filters or use different criteria.",
                conclusion="No matching records were found.",
                model="System",
                error=None,
            )

            return AnalysisResult(
                metadata=empty_metadata,
                summary=empty_summary,
                explanation=empty_explanation,
                trends=[],
                anomalies=[],
                recommendations=[],
                kpis=[],
                insights=[],
                charts=[],
                statistics=[],
            )

        # -------------------------------------------------
        # Automatic Column Selection
        # -------------------------------------------------

        selected = self.column_selector.select(
            dataframe
        )

        if selected.metric is None:

            logger.info(
                "No numeric metric detected. Returning descriptive analysis."
            )

            metadata = AnalysisMetadata(

                question=question,

                total_rows=len(dataframe),

                total_columns=len(dataframe.columns),

                execution_time=round(
                    time.perf_counter() - start_time,
                    4,
                ),

                selected_metric=None,

                selected_category=selected.category,

                selected_datetime=selected.datetime,
            )

            summary = self.summary_generator.generate_empty_summary()

            summary.executive_summary = (
                "The query returned descriptive data. "
                "No numeric metric was available for statistical analysis."
            )

            explanation = ExplanationResult(

                success=True,

                overview=(
                    "The result contains descriptive information "
                    "rather than numerical measures."
                ),

                trends="Trend analysis is unavailable.",

                risks="No risks detected.",

                opportunities=(
                    "You can explore this data further using filters "
                    "or aggregation."
                ),

                recommendations="",

                conclusion=summary.executive_summary,

                model="System",

                error=None,
            )

            return AnalysisResult(

                metadata=metadata,

                summary=summary,

                explanation=explanation,

                trends=[],

                anomalies=[],

                recommendations=[],

                kpis=[],

                insights=[],

                charts=[],

                statistics=[],
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

        # ------------------------------------------
        # KPI Generation
        # ------------------------------------------

        kpis = self.kpi_generator.generate(
            dataframe
        )

        # ---------------------------------------------
        # Detect business columns
        # ---------------------------------------------

        business_columns = column_detector.detect(
            dataframe.columns.tolist()
        )

        # ---------------------------------------------
        # Generate intelligent insights
        # ---------------------------------------------

        insights = [
            BusinessInsight(**item)
            for item in self.insight_generator.generate(
                dataframe=dataframe,
                columns=business_columns,
            )
        ]

        statistics = self.statistic_generator.generate(
            dataframe
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
                insights=insights,
            )
        )

        logger.info(
            "%d recommendation(s) generated.",
            recommendations.total,
        )

        narrative = self.narrative_generator.generate(
            kpis=kpis,
            insights=insights,
        )

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
        summary.executive_summary = narrative

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
            trends=[trend],
            anomalies=[anomaly],
            recommendations=[recommendations],
            kpis=kpis,
            insights=insights,
            charts=[],
            statistics=statistics,
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
    ) -> bool:

        if dataframe is None:

            raise ValueError(
                "DataFrame cannot be None."
            )

        if len(dataframe.columns) == 0:

            raise ValueError(
                "DataFrame contains no columns."
            )

        return not dataframe.empty

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
