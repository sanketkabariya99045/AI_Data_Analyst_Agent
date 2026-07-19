"""
Dashboard API Models

Author:
Sanket Kabariya
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class DashboardKPIResponse(BaseModel):

    title: str

    value: Any

    description: str = ""


class DashboardChartResponse(BaseModel):

    title: str

    chart: dict | None

    chart_type: str

class DashboardTableResponse(BaseModel):
    """
    Dashboard table response.
    """

    title: str

    columns: list[str]

    rows: list[dict]
    
class DashboardSummaryResponse(BaseModel):

    overview: str

    recommendations: list[str]

    risks: list[str]

    opportunities: list[str]


class DashboardResponse(BaseModel):

    success: bool

    title: str

    description: str

    kpis: list[DashboardKPIResponse]

    charts: list[DashboardChartResponse]

    tables: list[DashboardTableResponse]

    summary: DashboardSummaryResponse

    metadata: dict