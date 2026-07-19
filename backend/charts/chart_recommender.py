"""
backend/charts/chart_recommender.py

Automatically selects the best chart
based on dataframe structure.
"""

from __future__ import annotations

import pandas as pd


class ChartRecommender:

    def recommend(
    self,
    dataframe: pd.DataFrame,
) -> str:

        if dataframe.empty:
            return "table"

        numeric = dataframe.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical = dataframe.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        datetime = dataframe.select_dtypes(
            include=["datetime64", "datetime64[ns]"]
        ).columns.tolist()

        # ----------------------------------------
        # Detect date-like column names
        # ----------------------------------------

        for column in dataframe.columns:

            name = column.lower()

            if any(
                word in name
                for word in [
                    "date",
                    "month",
                    "year",
                    "day",
                    "time",
                ]
            ):
                return "line"

        # ----------------------------------------

        if datetime and numeric:
            return "line"

        # ----------------------------------------

        if len(numeric) >= 2:
            return "scatter"

        # ----------------------------------------

        if len(categorical) >= 1 and len(numeric) >= 1:

            unique = dataframe[categorical[0]].nunique()

            if unique <= 6:
                return "pie"

            return "bar"

        # ----------------------------------------

        if len(numeric) == 1:
            return "histogram"

        return "table"


chart_recommender = ChartRecommender()