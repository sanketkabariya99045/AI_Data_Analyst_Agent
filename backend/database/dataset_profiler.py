"""
Enterprise Dataset Profiler.

Builds metadata describing a dataset
before it is sent to the LLM.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd


class DatasetProfiler:

    def profile(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:

        numeric = dataframe.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical = dataframe.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        datetime_columns = []

        for column in dataframe.columns:

            name = column.lower()

            if any(
                token in name
                for token in [
                    "date",
                    "time",
                    "month",
                    "year",
                ]
            ):
                datetime_columns.append(column)

        return {

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "numeric_columns": numeric,

            "categorical_columns": categorical,

            "datetime_columns": datetime_columns,

        }


dataset_profiler = DatasetProfiler()