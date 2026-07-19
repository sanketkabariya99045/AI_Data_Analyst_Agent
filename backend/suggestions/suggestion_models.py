"""
Suggestion Models

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel


class SuggestedQuestion(BaseModel):

    question: str

    category: str


class SuggestionResult(BaseModel):

    suggestions: List[SuggestedQuestion]