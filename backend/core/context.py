"""
backend/core/context.py

Enterprise Pipeline Context.

Shared state passed through every pipeline stage.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd
import plotly.graph_objects as go


@dataclass(slots=True)
class PipelineContext:
    """
    Shared pipeline context.

    Every stage reads from and writes to
    this object.
    """

    # --------------------------------------------------
    # Input
    # --------------------------------------------------

    question: str

    # --------------------------------------------------
    # Planner
    # --------------------------------------------------

    execution_plan: Any = None

    # --------------------------------------------------
    # SQL
    # --------------------------------------------------

    sql: str = ""

    validated_sql: str = ""

    # --------------------------------------------------
    # Query
    # --------------------------------------------------

    dataframe: pd.DataFrame | None = None

    # --------------------------------------------------
    # Analysis
    # --------------------------------------------------

    analysis: Any = None

    # --------------------------------------------------
    # Visualization
    # --------------------------------------------------

    figure: go.Figure | None = None

    chart_type: str = ""

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    warnings: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    error: str | None = None