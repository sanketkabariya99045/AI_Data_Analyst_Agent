"""
backend/charts/axis_selector.py

Enterprise Smart Axis Selector.

Chooses the most appropriate
X and Y axis using the
user question and dataframe.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd


class AxisSelector:

    def select(
        self,
        question: str,
        dataframe: pd.DataFrame,
    ) -> tuple[str, str | None]:

        question = question.lower()

        columns = {
            column.lower(): column
            for column in dataframe.columns
        }

        # --------------------------
        # Y Axis (measure)
        # --------------------------

        # --------------------------
        # Y Axis (measure)
        # --------------------------

        y_axis = None

        # First preference: numeric columns
        numeric_columns = dataframe.select_dtypes(
            include="number"
        ).columns.tolist()

        measure_keywords = [
            "sales",
            "revenue",
            "profit",
            "quantity",
            "discount",
            "cost",
            "price",
            "amount",
            "total",
        ]

        best_score = -1

        for column in numeric_columns:

            name = column.lower()

            score = 0

            for keyword in measure_keywords:

                if name == keyword:
                    score += 100
                elif name.endswith(keyword):
                    score += 80
                elif keyword in name:
                    score += 40

            # Prefer columns explicitly mentioned in the question
            if any(k in question for k in measure_keywords):
                if any(k in name for k in measure_keywords):
                    score += 20

            if score > best_score:
                best_score = score
                y_axis = column

        # Fallback
        if y_axis is None and numeric_columns:
            y_axis = numeric_columns[0]

        # --------------------------
        # X Axis (dimension)
        # --------------------------

        x_axis = None

        dimension_keywords = [

            "date",
            "month",
            "year",
            "day",
            "time",

            "region",
            "state",
            "city",
            "country",

            "category",
            "sub-category",

            "customer",
            "segment",

            "product",

        ]

        for keyword in dimension_keywords:

            for column in dataframe.columns:

                if keyword in column.lower():

                    if keyword in question:

                        x_axis = column
                        break

            if x_axis:
                break

        # fallback

        if x_axis is None:

            datetime = dataframe.select_dtypes(
                include=["datetime64", "datetime64[ns]"]
            ).columns.tolist()

            if datetime:

                x_axis = datetime[0]

        if x_axis is None:

            categorical = dataframe.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

            if categorical:

                x_axis = categorical[0]

        if x_axis is None:

            numeric = dataframe.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric:

                x_axis = numeric[0]

        # Prevent using the same column for both axes
        if x_axis == y_axis:

            for column in dataframe.columns:

                if column != y_axis:

                    if (
                        dataframe[column].dtype == "object"
                        or "date" in column.lower()
                        or "month" in column.lower()
                        or "year" in column.lower()
                    ):
                        x_axis = column
                        break
        return x_axis, y_axis


axis_selector = AxisSelector()