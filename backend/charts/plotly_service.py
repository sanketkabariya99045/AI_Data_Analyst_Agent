"""
Plotly Service

Responsible for creating Plotly visualizations.

Project:
AI Data Analyst
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from backend.charts.chart_models import ChartConfig, ChartType


class PlotlyService:
    """
    Creates Plotly charts.
    """

    # -------------------------------------------------
    # PUBLIC METHOD
    # -------------------------------------------------

    def create_chart(
        self,
        dataframe: pd.DataFrame,
        config: ChartConfig,
    ) -> go.Figure:
        """
        Create a Plotly chart based on ChartConfig.
        """

        if config.chart_type == ChartType.BAR:
            return self._bar(dataframe, config)

        elif config.chart_type == ChartType.LINE:
            return self._line(dataframe, config)

        elif config.chart_type == ChartType.SCATTER:
            return self._scatter(dataframe, config)

        elif config.chart_type == ChartType.PIE:
            return self._pie(dataframe, config)

        elif config.chart_type == ChartType.HISTOGRAM:
            return self._histogram(dataframe, config)

        elif config.chart_type == ChartType.BOX:
            return self._box(dataframe, config)

        elif config.chart_type == ChartType.AREA:
            return self._area(dataframe, config)

        elif config.chart_type == ChartType.HEATMAP:
            return self._heatmap(dataframe)

        raise ValueError(
            f"Unsupported chart: {config.chart_type}"
        )

    # -------------------------------------------------

    def _apply_layout(
        self,
        figure: go.Figure,
        config: ChartConfig,
    ) -> go.Figure:
        """
        Apply common layout.
        """

        figure.update_layout(

            title=config.title,

            xaxis_title=config.x_label,

            yaxis_title=config.y_label,

            template="plotly_white",

            hovermode="closest",

            legend_title_text="",

            margin=dict(

                l=40,

                r=40,

                t=60,

                b=40,

            )

        )

        return figure

    # -------------------------------------------------

    def _bar(
        self,
        dataframe,
        config,
    ):

        fig = px.bar(

            dataframe,

            x=config.x_axis,

            y=config.y_axis,

            color=config.color,

        )

        return self._apply_layout(
            fig,
            config,
        )

    # -------------------------------------------------

    def _line(
        self,
        dataframe,
        config,
    ):

        fig = px.line(

            dataframe,

            x=config.x_axis,

            y=config.y_axis,

            color=config.color,

            markers=True,

        )

        return self._apply_layout(
            fig,
            config,
        )

    # -------------------------------------------------

    def _scatter(
        self,
        dataframe,
        config,
    ):

        fig = px.scatter(

            dataframe,

            x=config.x_axis,

            y=config.y_axis,

            color=config.color,

        )

        return self._apply_layout(
            fig,
            config,
        )

    # -------------------------------------------------

    def _pie(
        self,
        dataframe,
        config,
    ):

        fig = px.pie(

            dataframe,

            names=config.x_axis,

            values=config.y_axis,

        )

        return self._apply_layout(
            fig,
            config,
        )

    # -------------------------------------------------

    def _histogram(
        self,
        dataframe,
        config,
    ):

        fig = px.histogram(

            dataframe,

            x=config.x_axis,

        )

        return self._apply_layout(
            fig,
            config,
        )

    # -------------------------------------------------

    def _box(
        self,
        dataframe,
        config,
    ):

        fig = px.box(

            dataframe,

            x=config.x_axis,

            y=config.y_axis,

        )

        return self._apply_layout(
            fig,
            config,
        )

    # -------------------------------------------------

    def _area(
        self,
        dataframe,
        config,
    ):

        fig = px.area(

            dataframe,

            x=config.x_axis,

            y=config.y_axis,

        )

        return self._apply_layout(
            fig,
            config,
        )

    # -------------------------------------------------

    def _heatmap(
        self,
        dataframe,
    ):

        correlation = dataframe.corr(
            numeric_only=True
        )

        fig = px.imshow(

            correlation,

            text_auto=True,

            aspect="auto",

        )

        fig.update_layout(

            title="Correlation Heatmap"

        )

        return fig


plotly_service = PlotlyService()