"""
backend/models/api_models.py

API request and response models.

These models define the public contract between
the FastAPI backend and the Streamlit frontend.

Internal backend models (AnalysisResult, KPIResult,
TrendResult, etc.) should never be returned directly.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from backend.suggestions.suggestion_models import (
    SuggestedQuestion,
)

# ==========================================================
# BASE MODEL
# ==========================================================

class APIModel(BaseModel):
    """
    Base model for all API request/response DTOs.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="forbid",
    )


# ==========================================================
# REQUEST MODELS
# ==========================================================

class AnalyzeRequest(APIModel):
    """
    Request received from the frontend.
    """

    question: str = Field(
        ...,
        description="Natural language business question."
    )


# ==========================================================
# RESPONSE MODELS
# ==========================================================

class AnalyzeResponse(APIModel):
    """
    Final response returned to the frontend.
    """

    success: bool

    question: str

    generated_sql: str

    query_result: list[dict[str, Any]] = Field(
        default_factory=list
    )

    summary: dict[str, Any] = Field(
        default_factory=dict
    )

    explanation: dict[str, Any] = Field(
        default_factory=dict
    )

    trends: list[dict[str, Any]] = Field(
        default_factory=list
    )

    anomalies: list[dict[str, Any]] = Field(
        default_factory=list
    )

    recommendations: list[dict[str, Any]] = Field(
        default_factory=list
    )

    kpis: list[dict[str, Any]] = Field(
        default_factory=list
    )

    insights: list[dict[str, Any]] = Field(
        default_factory=list
    )

    statistics: list[dict[str, Any]] = Field(
        default_factory=list
    )
    
    executive_summary: str | None = None

    chart: dict[str, Any] | None = None

    chart_type: str | None = None

    warnings: list[str] = Field(
        default_factory=list
    )

    error: str | None = None


# ==========================================================
# UPLOAD RESPONSE
# ==========================================================

class UploadFileInfo(APIModel):
    """
    Information about a processed file.
    """

    table_name: str

    rows: int

    columns: list[str]

class DatasetProfileResponse(APIModel):
    """
    Dataset profiling information.
    """

    rows: int

    columns: int

    memory_mb: float

    duplicate_rows: int

    missing_values: int

    numeric_columns: list[str] = Field(default_factory=list)

    categorical_columns: list[str] = Field(default_factory=list)

    datetime_columns: list[str] = Field(default_factory=list)

    business_columns: list[str] = Field(default_factory=list)
    
class UploadResponse(APIModel):
    """
    Upload API response.
    """

    success: bool

    total_files: int

    files: list[UploadFileInfo]

    profile: DatasetProfileResponse | None = None

    suggestions: list[SuggestedQuestion] = Field(
        default_factory=list
    )