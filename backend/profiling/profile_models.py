"""
Dataset Profile Models

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel


class DatasetProfile(BaseModel):

    rows: int

    columns: int

    memory_mb: float

    duplicate_rows: int

    missing_values: int

    numeric_columns: List[str]

    categorical_columns: List[str]

    datetime_columns: List[str]

    business_columns: List[str]