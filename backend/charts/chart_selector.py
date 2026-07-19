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

from backend.charts.axis_selector import (
    axis_selector,
)

from backend.charts.chart_intelligence import (
    chart_intelligence,
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


        if request.preferred_chart:

            chart_type = request.preferred_chart

        else:

            recommendation = chart_intelligence.recommend(
                question=request.question,
                dataframe=request.dataframe,
            )

            chart_map = {
                "bar": ChartType.BAR,
                "line": ChartType.LINE,
                "pie": ChartType.PIE,
                "scatter": ChartType.SCATTER,
                "histogram": ChartType.HISTOGRAM,
                "box": ChartType.BOX,
                "area": ChartType.AREA,
                "heatmap": ChartType.HEATMAP,
                "table": ChartType.BAR,
            }

            chart_type = chart_map.get(
                recommendation,
                ChartType.BAR,
            )
            print("FINAL CHART TYPE:", chart_type)

        x_axis, y_axis = axis_selector.select(
            question=request.question,
            dataframe=request.dataframe,
        )

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