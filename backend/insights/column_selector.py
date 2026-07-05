"""
Column Selector

Automatically identifies the most appropriate
columns for business analysis.

Project:
AI Data Analyst
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd
from pandas.api.types import (
    is_numeric_dtype,
    is_datetime64_any_dtype,
)


@dataclass
class SelectedColumns:
    """
    Selected columns for downstream analytics.
    """

    metric: Optional[str]

    category: Optional[str]

    datetime: Optional[str]


class ColumnSelector:
    """
    Detects important columns from a DataFrame.
    """

    METRIC_PRIORITY = [
        "revenue",
        "sales",
        "profit",
        "amount",
        "income",
        "price",
        "cost",
        "total",
        "value",
        "quantity",
        "count",
    ]

    DATE_PRIORITY = [
        "date",
        "day",
        "month",
        "year",
        "quarter",
        "time",
        "timestamp",
    ]

    # -------------------------------------------------

    def select(
        self,
        dataframe: pd.DataFrame,
    ) -> SelectedColumns:
        """
        Automatically select metric, category,
        and datetime columns.
        """

        metric = self._select_metric(dataframe)

        category = self._select_category(dataframe)

        datetime = self._select_datetime(dataframe)

        return SelectedColumns(
            metric=metric,
            category=category,
            datetime=datetime,
        )

    # -------------------------------------------------

    def _select_metric(
        self,
        dataframe: pd.DataFrame,
    ) -> Optional[str]:

        columns = list(dataframe.columns)

        # Priority by column name
        for keyword in self.METRIC_PRIORITY:

            for column in columns:

                if keyword in column.lower():

                    if is_numeric_dtype(
                        dataframe[column]
                    ):
                        return column

        # Fallback
        for column in columns:

            if is_numeric_dtype(
                dataframe[column]
            ):
                return column

        return None

    # -------------------------------------------------

    def _select_datetime(
        self,
        dataframe: pd.DataFrame,
    ) -> Optional[str]:

        columns = list(dataframe.columns)

        for keyword in self.DATE_PRIORITY:

            for column in columns:

                if keyword in column.lower():
                    return column

        for column in columns:

            if is_datetime64_any_dtype(
                dataframe[column]
            ):
                return column

        return None

    # -------------------------------------------------

    def _select_category(
        self,
        dataframe: pd.DataFrame,
    ) -> Optional[str]:

        columns = list(dataframe.columns)

        ignored = {
            self._select_metric(dataframe),
            self._select_datetime(dataframe),
        }

        for column in columns:

            if column in ignored:
                continue

            if not is_numeric_dtype(
                dataframe[column]
            ):
                return column

        return None


column_selector = ColumnSelector()