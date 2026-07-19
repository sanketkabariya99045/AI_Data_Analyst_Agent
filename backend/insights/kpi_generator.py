"""
backend/insights/kpi_generator.py

Enterprise Intelligent KPI Generator

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd

from backend.intelligence.business_kpis import (
    business_kpi_generator,
)
from backend.intelligence.column_detector import (
    column_detector,
)
from backend.models.analysis_models import KPIResult


class KPIGenerator:
    """
    Enterprise KPI Generator.

    Workflow
    --------

    DataFrame
        ↓
    Detect Business Columns
        ↓
    Generate Business KPIs
        ↓
    Fallback Generic KPIs
    """

    def generate(
        self,
        dataframe: pd.DataFrame,
    ) -> list[KPIResult]:

        # ---------------------------------------------
        # Detect business columns
        # ---------------------------------------------

        detected_columns = column_detector.detect(
            dataframe.columns.tolist()
        )

        # ---------------------------------------------
        # Business KPIs
        # ---------------------------------------------

        business_kpis = (
            business_kpi_generator.generate(
                dataframe=dataframe,
                columns=detected_columns,
            )
        )

        # If business KPIs exist,
        # return them directly.
        if business_kpis:

            return business_kpis

        # ---------------------------------------------
        # Generic KPIs (Fallback)
        # ---------------------------------------------

        return self._generate_generic_kpis(
            dataframe
        )

    # ==================================================
    # Generic KPI Generator
    # ==================================================

    def _generate_generic_kpis(
        self,
        dataframe: pd.DataFrame,
    ) -> list[KPIResult]:

        kpis: list[KPIResult] = []

        # Rows

        kpis.append(

            KPIResult(

                name="Rows",

                value=len(dataframe),

                description="Rows returned",
            )

        )

        numeric = dataframe.select_dtypes(
            include="number"
        )

        if numeric.empty:

            return kpis

        first_column = numeric.columns[0]

        series = numeric[first_column]

        kpis.append(

            KPIResult(

                name="Total",

                value=round(
                    float(series.sum()),
                    2,
                ),

                description=f"Total {first_column}",
            )

        )

        kpis.append(

            KPIResult(

                name="Average",

                value=round(
                    float(series.mean()),
                    2,
                ),

                description=f"Average {first_column}",
            )

        )

        kpis.append(

            KPIResult(

                name="Maximum",

                value=round(
                    float(series.max()),
                    2,
                ),

                description=f"Maximum {first_column}",
            )

        )

        return kpis


kpi_generator = KPIGenerator()