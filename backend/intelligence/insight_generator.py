"""
backend/intelligence/insight_generator.py

Enterprise Insight Generator.

Generates intelligent business insights
from detected business columns.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import pandas as pd


class InsightGenerator:
    """
    Enterprise Business Insight Generator.
    """

    def generate(
        self,
        dataframe: pd.DataFrame,
        columns: dict[str, str],
    ) -> list[dict]:
        """
        Generate business insights.
        """

        insights: list[dict] = []

        # ==================================================
        # Revenue Insight
        # ==================================================

        if "sales" in columns:

            sales = columns["sales"]

            insights.append(
                {
                    "title": "Revenue",
                    "description": (
                        f"Total revenue is "
                        f"{dataframe[sales].sum():,.2f}."
                    ),
                    "severity": "High",
                }
            )

        # ==================================================
        # Profit Insight
        # ==================================================

        if "profit" in columns:

            profit = columns["profit"]

            insights.append(
                {
                    "title": "Profit",
                    "description": (
                        f"Total profit is "
                        f"{dataframe[profit].sum():,.2f}."
                    ),
                    "severity": "High",
                }
            )

        # ==================================================
        # Customer Insight
        # ==================================================

        if "customer" in columns:

            customer = columns["customer"]

            insights.append(
                {
                    "title": "Customers",
                    "description": (
                        f"There are "
                        f"{dataframe[customer].nunique()} "
                        f"unique customers."
                    ),
                    "severity": "Medium",
                }
            )

        # ==================================================
        # Region Insight
        # ==================================================

        if "region" in columns:

            region = columns["region"]

            top = (
                dataframe[region]
                .value_counts()
                .idxmax()
            )

            insights.append(
                {
                    "title": "Top Region",
                    "description": (
                        f"{top} contains the highest number of records."
                    ),
                    "severity": "Medium",
                }
            )

        # ==================================================
        # Sales by Region
        # ==================================================

        if (
            "sales" in columns
            and "region" in columns
        ):

            region = columns["region"]
            sales = columns["sales"]

            top_region, value = self._highest_group(
                dataframe,
                region,
                sales,
            )

            insights.append(
                {
                    "title": "Highest Revenue Region",
                    "description": (
                        f"{top_region} generated "
                        f"{value:,.2f} in revenue."
                    ),
                    "severity": "High",
                }
            )

        # ==================================================
        # Profit by Category
        # ==================================================

        if (
            "profit" in columns
            and "category" in columns
        ):

            category = columns["category"]
            profit = columns["profit"]

            top_category, value = self._highest_group(
                dataframe,
                category,
                profit,
            )

            insights.append(
                {
                    "title": "Most Profitable Category",
                    "description": (
                        f"{top_category} generated "
                        f"{value:,.2f} total profit."
                    ),
                    "severity": "High",
                }
            )

        # ==================================================
        # Average Discount
        # ==================================================

        if "discount" in columns:

            discount = columns["discount"]

            avg_discount = self._average(
                dataframe,
                discount,
            )

            insights.append(
                {
                    "title": "Average Discount",
                    "description": (
                        f"Average discount is "
                        f"{avg_discount:.2f}."
                    ),
                    "severity": "Low",
                }
            )

        return insights

    # ==================================================
    # Helper Methods
    # ==================================================

    def _highest_group(
        self,
        dataframe: pd.DataFrame,
        group_column: str,
        value_column: str,
    ):

        grouped = (
            dataframe
            .groupby(group_column)[value_column]
            .sum()
        )

        if grouped.empty:
            return None, 0.0

        return (
            grouped.idxmax(),
            float(grouped.max()),
        )

    # --------------------------------------------------

    def _lowest_group(
        self,
        dataframe: pd.DataFrame,
        group_column: str,
        value_column: str,
    ):

        grouped = (
            dataframe
            .groupby(group_column)[value_column]
            .sum()
        )

        if grouped.empty:
            return None, 0.0

        return (
            grouped.idxmin(),
            float(grouped.min()),
        )

    # --------------------------------------------------

    def _average(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> float:

        return float(
            dataframe[column].mean()
        )


# ==================================================
# Singleton
# ==================================================

insight_generator = InsightGenerator()