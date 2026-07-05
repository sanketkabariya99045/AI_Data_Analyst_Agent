"""
backend/models/analysis_models.py

Enterprise data models for the AI Business Intelligence Platform.

These models define the contracts exchanged between
the Insight Engine, Chart Engine, Forecast Engine,
Dashboard Engine, API layer, and frontend.

Author: Sanket Kabariya
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field, ConfigDict


# ==========================================================
# ENUMS
# ==========================================================

class TrendDirection(str, Enum):
    """Business trend direction."""

    INCREASING = "Increasing"
    DECREASING = "Decreasing"
    STABLE = "Stable"


class SeverityLevel(str, Enum):
    """Severity level."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class PriorityLevel(str, Enum):
    """Recommendation priority."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# ==========================================================
# BASE MODEL
# ==========================================================

class BaseAnalysisModel(BaseModel):
    """
    Base model shared across the analysis engine.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="forbid",
    )


# ==========================================================
# ANALYSIS METADATA
# ==========================================================

class AnalysisMetadata(BaseAnalysisModel):
    """
    Metadata describing the current analysis.
    """

    question: str = Field(
        ...,
        description="Original user question."
    )

    generated_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    total_rows: int = Field(
        ge=0
    )

    total_columns: int = Field(
        ge=0
    )

    execution_time: Optional[float] = Field(
        default=None,
        ge=0,
        description="Execution time in seconds."
    )

    selected_metric: Optional[str] = None

    selected_category: Optional[str] = None

    selected_datetime: Optional[str] = None


# ==========================================================
# TREND ANALYSIS
# ==========================================================

class TrendResult(BaseAnalysisModel):
    """
    Business trend detection result.
    """

    trend: TrendDirection

    percentage_change: float

    first_value: float

    last_value: float

    message: str


# ==========================================================
# ANOMALY ANALYSIS
# ==========================================================

class Anomaly(BaseAnalysisModel):
    """
    Single detected anomaly.
    """

    index: int

    value: float

    z_score: float


class AnomalyResult(BaseAnalysisModel):
    """
    Complete anomaly analysis.
    """

    total_rows: int

    anomaly_count: int

    anomalies: List[Anomaly] = Field(
        default_factory=list
    )

    message: str


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

class Recommendation(BaseAnalysisModel):
    """
    Single business recommendation.
    """

    priority: PriorityLevel

    category: str

    recommendation: str


class RecommendationResult(BaseAnalysisModel):
    """
    Recommendation engine output.
    """

    total: int

    recommendations: List[
        Recommendation
    ] = Field(default_factory=list)


# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

class SummaryResult(BaseAnalysisModel):
    """
    Structured executive summary.
    """
    executive_summary: str = ""
    
    overview: str

    trend_summary: str

    anomaly_summary: str

    recommendation_summary: List[
        str
    ] = Field(default_factory=list)


# ==========================================================
# AI EXPLANATION
# ==========================================================

class ExplanationResult(BaseAnalysisModel):

    success: bool

    overview: str

    trends: str

    risks: str

    opportunities: str

    recommendations: str

    conclusion: str

    model: str

    error: Optional[str]
    

# ==========================================================
# KPI MODELS
# ==========================================================

class KPIResult(BaseAnalysisModel):
    """
    Represents a business KPI extracted from
    the analysis.
    """

    name: str

    value: Any

    unit: Optional[str] = None

    change_percentage: Optional[float] = None

    description: Optional[str] = None


# ==========================================================
# CHART MODELS
# ==========================================================

class ChartRecommendation(BaseAnalysisModel):
    """
    Recommended visualization.
    """

    chart_type: str

    title: str

    x_column: Optional[str] = None

    y_column: Optional[str] = None

    color_column: Optional[str] = None

    description: Optional[str] = None


class ChartMetadata(BaseAnalysisModel):
    """
    Metadata about generated charts.
    """

    total_charts: int = 0

    interactive: bool = True

    library: str = "Plotly"


# ==========================================================
# BUSINESS STATISTICS
# ==========================================================

class BusinessStatistic(BaseAnalysisModel):
    """
    Generic business statistic.
    """

    metric: str

    value: Any

    description: Optional[str] = None


# ==========================================================
# BUSINESS INSIGHT
# ==========================================================

class BusinessInsight(BaseAnalysisModel):
    """
    High-level business insight.
    """

    title: str

    description: str

    impact: Optional[str] = None

    severity: SeverityLevel = SeverityLevel.LOW


# ==========================================================
# FINAL ANALYSIS RESULT
# ==========================================================

class AnalysisResult(BaseAnalysisModel):
    """
    Final result returned by the Insight Engine.

    This model is passed to

    • Chart Agent
    • Forecast Agent
    • Dashboard Agent
    • API
    • Frontend
    """

    metadata: AnalysisMetadata

    summary: SummaryResult

    explanation: ExplanationResult

    trends: List[TrendResult] = Field(
        default_factory=list
    )

    anomalies: List[AnomalyResult] = Field(
        default_factory=list
    )

    recommendations: List[
        RecommendationResult
    ] = Field(default_factory=list)

    kpis: List[KPIResult] = Field(
        default_factory=list
    )

    insights: List[
        BusinessInsight
    ] = Field(default_factory=list)

    charts: List[
        ChartRecommendation
    ] = Field(default_factory=list)

    statistics: List[
        BusinessStatistic
    ] = Field(default_factory=list)


# ==========================================================
# REQUEST MODEL
# ==========================================================

class AnalysisRequest(BaseAnalysisModel):
    """
    Request received from API.
    """

    question: str

    table_name: str

    include_charts: bool = True

    include_insights: bool = True

    include_statistics: bool = True


# ==========================================================
# API RESPONSE MODEL
# ==========================================================

class AnalysisResponse(BaseAnalysisModel):
    """
    Final response returned to frontend.
    """

    success: bool

    sql_query: Optional[str] = None

    analysis: Optional[
        AnalysisResult
    ] = None

    error: Optional[str] = None