"""
backend/dashboard/dashboard_kpi_engine.py

Enterprise Dashboard KPI Engine.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging

import pandas as pd

from backend.dashboard.dashboard_models import DashboardKPI
from backend.services.sql_execution_service import SQLExecutionResponse

logger = logging.getLogger(__name__)


class DashboardKPIEngine:
    """
    Extract KPI cards from SQL results.
    """

    def build(
        self,
        results: list[SQLExecutionResponse],
    ) -> list[DashboardKPI]:

        logger.info(
            "Building dashboard KPIs."
        )

        kpis: list[DashboardKPI] = []

        for result in results:

            if not result.success:
                continue

            if result.dataframe is None:
                continue

            dataframe = result.dataframe

            if dataframe.empty:
                continue

            # --------------------------------------
            # Single row → one KPI per column
            # --------------------------------------

            if dataframe.shape[0] == 1:

                row = dataframe.iloc[0]

                for column in dataframe.columns:

                    kpis.append(

                        DashboardKPI(

                            title=column,

                            value=row[column],

                            description=result.question,

                        )

                    )

                continue

            # --------------------------------------
            # Single scalar
            # --------------------------------------

            if (
                dataframe.shape[0] == 1
                and dataframe.shape[1] == 1
            ):

                kpis.append(

                    DashboardKPI(

                        title=result.question,

                        value=dataframe.iat[0, 0],

                        description=result.sql,

                    )

                )

                continue

            # --------------------------------------
            # Multi-row datasets
            # --------------------------------------

            value = self._extract_value(
                dataframe,
            )

            kpis.append(

                DashboardKPI(

                    title=result.question,

                    value=value,

                    description=result.sql,

                )

            )

        logger.info(
            "Generated %d KPIs.",
            len(kpis),
        )

        return kpis

    # -----------------------------------------------------

    @staticmethod
    def _extract_value(
        dataframe: pd.DataFrame,
    ):

        if dataframe.empty:
            return "-"

        if (
            dataframe.shape[0] == 1
            and dataframe.shape[1] == 1
        ):
            return dataframe.iat[0, 0]

        numeric = dataframe.select_dtypes(
            include="number",
        )

        if not numeric.empty:

            return round(
                numeric.iloc[:, 0].sum(),
                2,
            )

        return f"{len(dataframe)} records"


dashboard_kpi_engine = DashboardKPIEngine()