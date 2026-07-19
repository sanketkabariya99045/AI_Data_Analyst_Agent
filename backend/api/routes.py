"""
backend/api/routes.py

Enterprise REST API for the
AI Business Intelligence Platform.
"""

from __future__ import annotations


from typing import Any
import json
import traceback
from fastapi import APIRouter, File, HTTPException, UploadFile
from plotly.utils import PlotlyJSONEncoder
from backend.models.dashboard_api_models import (
    DashboardResponse,
    DashboardKPIResponse,
    DashboardChartResponse,
    DashboardTableResponse,
    DashboardSummaryResponse,
)
from backend.agents.agent_manager import agent_manager
from backend.models.api_models import (
    AnalyzeRequest,
    AnalyzeResponse,
    UploadFileInfo,
    UploadResponse,
)
from backend.services.upload_service import UploadService
from backend.dashboard.dashboard_agent import (
    dashboard_agent,
)



from backend.models.dashboard_api_models import (
    DashboardChartResponse,
)

from backend.utils.chart_serializer import (
    serialize_chart,
)
from backend.models.dashboard_api_models import (
    DashboardResponse,
)
from backend.models.dashboard_api_models import (
    DashboardResponse,
)
from backend.utils.json_serializer import (
    to_python,
)
from backend.dashboard.dashboard_service import (
    dashboard_service,
)
router = APIRouter(
    prefix="/api",
    tags=["AI Data Analyst"],
)

upload_service = UploadService()


# ==========================================================
# Helpers
# ==========================================================

def safe_json(value: Any):
    """
    Convert Plotly, NumPy and Pandas objects into
    normal Python objects.
    """
    return json.loads(
        json.dumps(
            value,
            cls=PlotlyJSONEncoder,
        )
    )


# ==========================================================
# Dashboard Helpers
# ==========================================================


def build_chart_response(chart):
    """
    Convert DashboardChart into API response.
    """

    return DashboardChartResponse(

        title=chart.title,

        chart=serialize_chart(
            chart.figure,
        ),

        chart_type=chart.chart_type,

    )

# ==========================================================
# Upload
# ==========================================================


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_file(
    file: UploadFile = File(...)
):
    try:

        result = await upload_service.process_files([file])

        uploaded_files = []

        for item in result:

            if not item["sheets"]:
                continue

            first_sheet = item["sheets"][0]
            profile = first_sheet.get("profile")

            suggestions = first_sheet.get(
                "suggestions",
                [],
            )

            uploaded_files.append(

                UploadFileInfo(
                    table_name=item["tables"][0],
                    rows=first_sheet["rows"],
                    columns=first_sheet["column_names"],
                )

            )

        return UploadResponse(

            success=True,

            total_files=len(uploaded_files),

            files=uploaded_files,

            profile=profile,

            suggestions=suggestions,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ==========================================================
# Analyze
# ==========================================================

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
async def analyze(
    request: AnalyzeRequest,
):

    try:

        response = agent_manager.process(
            question=request.question,
        )

        if not response.success:

            raise HTTPException(
                status_code=400,
                detail=response.error or "Analysis failed.",
            )

        analysis = response.analysis

        # --------------------------------------------------
        # Chart
        # --------------------------------------------------

        chart = None

        if (
            analysis is not None
            and analysis.figure is not None
        ):
            chart = json.loads(
                json.dumps(
                    analysis.figure,
                    cls=PlotlyJSONEncoder,
                )
            )

        # --------------------------------------------------
        # Query Result
        # --------------------------------------------------

        query_result = []

        if response.query_result is not None:
            query_result = safe_json(
                response.query_result.to_dict(
                    orient="records"
                )
            )
        kpi_payload = [
            kpi.model_dump()
            for kpi in analysis.analysis.kpis
        ]

        # --------------------------------------------------
        # Build API Response
        # --------------------------------------------------

        response = AnalyzeResponse(
            success=True,
            question=response.question,
            generated_sql=response.sql,
            query_result=query_result,
            summary=safe_json(
                analysis.analysis.summary.model_dump(mode="json")
            ),
            explanation=safe_json(
                analysis.analysis.explanation.model_dump(mode="json")
            ),
            trends=safe_json(
                [t.model_dump(mode="json") for t in analysis.analysis.trends]
            ),
            anomalies=safe_json(
                [a.model_dump(mode="json")
                 for a in analysis.analysis.anomalies]
            ),
            recommendations=safe_json(
                [r.model_dump(mode="json")
                 for r in analysis.analysis.recommendations]
            ),
            kpis=kpi_payload,
            insights=safe_json(
                [i.model_dump(mode="json") for i in analysis.analysis.insights]
            ),

            statistics=safe_json(
                [s.model_dump(mode="json")
                 for s in analysis.analysis.statistics]
            ),

            executive_summary=analysis.analysis.summary.executive_summary,
            chart=chart,          # <-- IMPORTANT
            chart_type=None,
            warnings=[],
            error=None,
        )
        return response

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

# ==========================================================
# Dashboard Builder
# ==========================================================


@router.post(
    "/dashboard",
    response_model=DashboardResponse,
)
async def dashboard(
    request: AnalyzeRequest,
):

    try:

        dashboard = dashboard_service.build_dashboard(
            request.question,
        )

        return DashboardResponse(

            success=True,

            title=dashboard.title,

            description=dashboard.description,

            kpis=[

                DashboardKPIResponse(

                    title=kpi.title,

                    value=to_python(
                        kpi.value,
                    ),

                    description=kpi.description,

                )

                for kpi in dashboard.kpis

            ],

            charts=[

                build_chart_response(chart)

                for chart in dashboard.charts

            ],

            tables=[

                DashboardTableResponse(

                    title=table.title,

                    columns=table.columns,

                    rows=to_python(
                        table.rows
                    ),

                )

                for table in dashboard.tables

            ],
            
            summary=DashboardSummaryResponse(

                overview=dashboard.summary.overview,

                recommendations=dashboard.summary.recommendations,

                risks=dashboard.summary.risks,

                opportunities=dashboard.summary.opportunities,

            ),

            metadata=to_python(
                dashboard.metadata
            )

        )

    except Exception as error:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
