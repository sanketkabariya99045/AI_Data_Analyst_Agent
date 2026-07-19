"""
backend/core/result.py

Enterprise Pipeline Result.

Standard response returned by every pipeline.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.core.context import PipelineContext


# ==========================================================
# Pipeline Result
# ==========================================================

@dataclass(slots=True)
class PipelineResult:
    """
    Final pipeline execution result.
    """

    success: bool

    context: PipelineContext

    execution_time: float = 0.0

    stages_completed: int = 0

    warnings: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    error: str | None = None
    
    # --------------------------------------------------
    # Timing
    # --------------------------------------------------

    started_at: float = 0.0

    finished_at: float = 0.0