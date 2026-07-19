"""
Dataset Profiler

Generates statistics describing a dataset.

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd

from backend.profiling.profile_models import DatasetProfile
from backend.profiling.business_column_detector import (
    business_column_detector,
)

class DatasetProfiler:
    """
    Generates a complete profile
    for a pandas DataFrame.
    """

    def profile(
        self,
        dataframe: pd.DataFrame,
    ) -> DatasetProfile:

        rows = len(dataframe)

        columns = len(dataframe.columns)

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        missing_values = int(
            dataframe.isna().sum().sum()
        )

        memory_mb = round(

            dataframe.memory_usage(
                deep=True
            ).sum()

            / (1024 * 1024),

            2,
        )

        # -----------------------------
        # Numeric
        # -----------------------------

        numeric_columns = list(

            dataframe.select_dtypes(

                include="number"

            ).columns

        )

        # -----------------------------
        # Date
        # -----------------------------

        datetime_columns = list(

            dataframe.select_dtypes(

                include=[
                    "datetime64",
                    "datetime64[ns]",
                ]

            ).columns

        )

        # -----------------------------
        # Categorical
        # -----------------------------

        categorical_columns = [

            column

            for column in dataframe.columns

            if column

            not in numeric_columns

            and column

            not in datetime_columns

        ]
        
        business_columns = business_column_detector.detect(
            list(dataframe.columns)
        )
        
        return DatasetProfile(

            rows=rows,

            columns=columns,

            memory_mb=memory_mb,

            duplicate_rows=duplicate_rows,

            missing_values=missing_values,

            numeric_columns=numeric_columns,

            categorical_columns=categorical_columns,

            datetime_columns=datetime_columns,

            business_columns=business_columns,
        )


dataset_profiler = DatasetProfiler()