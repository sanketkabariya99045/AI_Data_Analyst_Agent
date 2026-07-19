"""
backend/intelligence/business_kpis.py

Enterprise Business KPI Generator.

Generates intelligent business KPIs
based on detected business columns.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd

from backend.models.analysis_models import KPIResult


class BusinessKPIGenerator:
    """
    Generate business KPIs from detected columns.
    """

    def generate(
        self,
        dataframe: pd.DataFrame,
        columns: dict[str, str],
    ) -> list[KPIResult]:

        kpis: list[KPIResult] = []

        # ==================================================
        # Sales
        # ==================================================

        # ==================================================
        # Sales
        # ==================================================

        if "sales" in columns:

            sales_col = columns["sales"]

            if (
                sales_col in dataframe.columns
                and pd.api.types.is_numeric_dtype(dataframe[sales_col])
            ):

                kpis.append(
                    KPIResult(
                        name="Total Sales",
                        value=round(
                            float(dataframe[sales_col].sum()),
                            2,
                        ),
                        description="Total revenue",
                    )
                )

        # ==================================================
        # Profit
        # ==================================================

        if "profit" in columns:

            profit_col = columns["profit"]

            kpis.append(

                KPIResult(

                    name="Total Profit",

                    value=round(
                        float(
                            dataframe[profit_col].sum()
                        ),
                        2,
                    ),

                    description="Overall profit",
                )
            )

        # ==================================================
        # Quantity
        # ==================================================

        if "quantity" in columns:

            quantity_col = columns["quantity"]

            kpis.append(

                KPIResult(

                    name="Total Quantity",

                    value=int(
                        dataframe[
                            quantity_col
                        ].sum()
                    ),

                    description="Items sold",
                )
            )

        # ==================================================
        # Customers
        # ==================================================

        if "customer" in columns:

            customer_col = columns["customer"]

            kpis.append(

                KPIResult(

                    name="Customers",

                    value=int(
                        dataframe[
                            customer_col
                        ].nunique()
                    ),

                    description="Unique customers",
                )
            )

        # ==================================================
        # Orders
        # ==================================================

        if "order" in columns:

            order_col = columns["order"]

            kpis.append(

                KPIResult(

                    name="Orders",

                    value=int(
                        dataframe[
                            order_col
                        ].nunique()
                    ),

                    description="Total orders",
                )
            )

        # ==================================================
        # Average Discount
        # ==================================================

        if "discount" in columns:

            discount_col = columns["discount"]

            kpis.append(

                KPIResult(

                    name="Average Discount",

                    value=round(
                        float(
                            dataframe[
                                discount_col
                            ].mean()
                        ),
                        2,
                    ),

                    description="Average discount",
                )
            )

        return kpis


business_kpi_generator = BusinessKPIGenerator()