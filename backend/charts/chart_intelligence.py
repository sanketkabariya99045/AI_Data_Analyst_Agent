"""
backend/charts/chart_intelligence.py

Enterprise Chart Intelligence Engine.

Determines the best visualization
using both the user's question and
the query result.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd


class ChartIntelligence:
    """
    AI Chart Recommendation Engine.
    """

    def recommend(
        self,
        question: str,
        dataframe: pd.DataFrame,
    ) -> str:

        question = question.lower()

        # ---------------------------------
        # Question-based rules
        # ---------------------------------

        if any(
            word in question
            for word in [
                "trend",
                "monthly",
                "daily",
                "yearly",
                "over time",
                "timeline",
            ]
        ):
            return "line"

        if any(
            word in question
            for word in [
                "distribution",
                "spread",
            ]
        ):
            return "histogram"

        if any(
            word in question
            for word in [
                "relationship",
                "correlation",
                "vs",
                "versus",
            ]
        ):
            return "scatter"

        if any(
            word in question
            for word in [
                "percentage",
                "share",
                "composition",
            ]
        ):
            return "pie"

        # ---------------------------------
        # DataFrame-based rules
        # ---------------------------------

        numeric = dataframe.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical = dataframe.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        # Detect date-like columns

        for column in dataframe.columns:

            name = column.lower()

            if any(
                token in name
                for token in [
                    "date",
                    "month",
                    "year",
                    "day",
                    "time",
                ]
            ):
                return "line"

        # Two numeric columns

        if len(numeric) >= 2:
            return "scatter"

        # Category + Value

        if len(categorical) >= 1 and len(numeric) >= 1:

            # Only use Pie when explicitly requested

            if any(
                word in question
                for word in [
                    "percentage",
                    "share",
                    "composition",
                    "pie",
                ]
            ):
                return "pie"

            return "bar"

        # One numeric

        if len(numeric) == 1:
            return "histogram"

        return "bar"


chart_intelligence = ChartIntelligence()