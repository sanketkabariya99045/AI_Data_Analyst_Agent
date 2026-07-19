"""
backend/utils/chart_serializer.py

Utilities for serializing Plotly figures.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import json

from plotly.utils import PlotlyJSONEncoder


def serialize_chart(figure):
    """
    Convert a Plotly figure into a JSON-serializable dictionary.
    """

    if figure is None:
        return None

    return json.loads(
        json.dumps(
            figure,
            cls=PlotlyJSONEncoder,
        )
    )