"""
backend/api/routes.py

Enterprise REST API for the
AI Business Intelligence Platform.
"""

from __future__ import annotations


from typing import Any
import json

from fastapi import APIRouter, File, HTTPException, UploadFile
from plotly.utils import PlotlyJSONEncoder

from backend.agents.agent_manager import agent_manager
from backend.models.api_models import (
    AnalyzeRequest,
    AnalyzeResponse,
    UploadFileInfo,
    UploadResponse,
)
from backend.services.upload_service import UploadService

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
                analysis.analysis.summary.model_dump(mode="json")
            ),
            trends=safe_json(
                [t.model_dump(mode="json") for t in analysis.analysis.trends]
            ),
            anomalies=safe_json(
                [a.model_dump(mode="json") for a in analysis.analysis.anomalies]
            ),
            recommendations=safe_json(
                [r.model_dump(mode="json") for r in analysis.analysis.recommendations]
            ),
            kpis=[],
            insights=[],
            statistics=[],
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