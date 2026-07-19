"""
Enterprise Dashboard Table Engine

Converts SQL results into dashboard tables.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging

from backend.dashboard.dashboard_models import (
    DashboardTable,
)

logger = logging.getLogger(__name__)


class DashboardTableEngine:

    def build(
        self,
        table_results,
    ) -> list[DashboardTable]:

        tables = []

        for result in table_results:

            try:

                dataframe = result.dataframe

                if dataframe.empty:

                    logger.warning(
                        "Empty table result: %s",
                        result.question,
                    )

                    continue

                table = DashboardTable(

                    title=result.question,

                    columns=list(
                        dataframe.columns
                    ),

                    rows=dataframe.to_dict(
                        orient="records",
                    ),

                )

                tables.append(
                    table
                )

            except Exception:

                logger.exception(
                    "Failed to build table."
                )

        return tables


dashboard_table_engine = DashboardTableEngine()