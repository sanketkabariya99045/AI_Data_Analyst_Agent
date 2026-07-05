"""
Chart Selector

Automatically selects the most suitable chart.

Project:
AI Data Analyst
"""

from __future__ import annotations

from typing import List

import pandas as pd

from backend.charts.chart_models import (
    ChartConfig,
    ChartRequest,
    ChartType,
    DatasetMetadata,
)


class ChartSelector:
    """
    Selects the best visualization.
    """

    # ---------------------------------------

    def analyze_dataset(
        self,
        dataframe: pd.DataFrame,
    ) -> DatasetMetadata:
        """
        Extract metadata from DataFrame.
        """

        numeric = dataframe.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical = dataframe.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        datetime = dataframe.select_dtypes(
            include=["datetime64"]
        ).columns.tolist()

        return DatasetMetadata(
            row_count=len(dataframe),
            column_count=len(dataframe.columns),
            numeric_columns=numeric,
            categorical_columns=categorical,
            datetime_columns=datetime,
        )

    # ---------------------------------------

    def select(
        self,
        request: ChartRequest,
    ) -> ChartConfig:
        """
        Determine best chart.
        """

        metadata = self.analyze_dataset(
            request.dataframe
        )

        question = request.question.lower()

        if request.preferred_chart:

            chart_type = request.preferred_chart

        elif "trend" in question or "over time" in question:

            chart_type = ChartType.LINE

        elif "distribution" in question:

            chart_type = ChartType.HISTOGRAM

        elif "relationship" in question or "correlation" in question:

            chart_type = ChartType.SCATTER

        elif "percentage" in question or "share" in question:

            chart_type = ChartType.PIE

        elif "heatmap" in question:

            chart_type = ChartType.HEATMAP

        else:

            chart_type = ChartType.BAR

        x_axis = self.choose_x(metadata)

        y_axis = self.choose_y(metadata)

        return ChartConfig(
            chart_type=chart_type,
            x_axis=x_axis,
            y_axis=y_axis,
            title=request.question.title(),
            x_label=x_axis,
            y_label=y_axis if y_axis else "",
        )

    # ---------------------------------------

    def choose_x(
        self,
        metadata: DatasetMetadata,
    ) -> str:
        """
        Select X-axis.
        """

        if metadata.datetime_columns:
            return metadata.datetime_columns[0]

        if metadata.categorical_columns:
            return metadata.categorical_columns[0]

        if metadata.numeric_columns:
            return metadata.numeric_columns[0]

        raise ValueError("No suitable X-axis found.")

    # ---------------------------------------

    def choose_y(
        self,
        metadata: DatasetMetadata,
    ) -> str | None:
        """
        Select Y-axis.
        """

        if metadata.numeric_columns:

            return metadata.numeric_columns[0]

        return None


chart_selector = ChartSelector()