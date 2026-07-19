"""
backend/intelligence/statistic_generator.py

Enterprise Statistics Generator.

Generates descriptive statistics for
business datasets.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd

from backend.models.analysis_models import BusinessStatistic


class StatisticGenerator:
    """
    Generate descriptive statistics.
    """

    def generate(
        self,
        dataframe: pd.DataFrame,
    ) -> list[BusinessStatistic]:

        statistics: list[BusinessStatistic] = []

        numeric = dataframe.select_dtypes(
            include="number"
        )

        if numeric.empty:
            return statistics

        for column in numeric.columns:

            series = numeric[column].dropna()

            if series.empty:
                continue

            statistics.extend(

                [

                    BusinessStatistic(

                        metric=f"{column} Mean",

                        value=round(
                            float(series.mean()),
                            2,
                        ),
                        description="Arithmetic mean"
                    ),

                    BusinessStatistic(

                        metric=f"{column} Median",

                        value=round(
                            float(series.median()),
                            2,
                        ),
                        description="Median value"
                    ),

                    BusinessStatistic(

                        metric=f"{column} Standard Deviation",

                        value=round(
                            float(series.std()),
                            2,
                        ),
                        description="Standard deviation"
                    ),

                    BusinessStatistic(

                        metric=f"{column} Minimum",

                        value=round(
                            float(series.min()),
                            2,
                        ),
                        description="Minimum observed value"
                    ),

                    BusinessStatistic(

                        metric=f"{column} Maximum",

                        value=round(
                            float(series.max()),
                            2,
                        ),
                        description="Maximum observed value"
                    ),

                    BusinessStatistic(

                        metric=f"{column} Q1",

                        value=round(
                            float(series.quantile(0.25)),
                            2,
                        ),
                        description="First quartile (25th percentile)"
                    ),

                    BusinessStatistic(

                        metric=f"{column} Q3",

                        value=round(
                            float(series.quantile(0.75)),
                            2,
                        ),
                        description="Third quartile (75th percentile)"
                    ),

                ]

            )

        return statistics


statistic_generator = StatisticGenerator()