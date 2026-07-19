"""
Business Column Detector

Automatically detects important business columns
from a dataset.

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

import re


class BusinessColumnDetector:
    """
    Detect common business columns.
    """

    COLUMN_PATTERNS = {

        "Sales": [
            "sales",
            "sale",
            "revenue",
            "amount",
            "income",
        ],

        "Profit": [
            "profit",
            "margin",
            "earnings",
        ],

        "Quantity": [
            "quantity",
            "qty",
            "units",
        ],

        "Discount": [
            "discount",
        ],

        "Customer": [
            "customer",
            "customer name",
            "client",
            "buyer",
        ],

        "Product": [
            "product",
            "product name",
            "item",
        ],

        "Category": [
            "category",
            "sub-category",
            "subcategory",
        ],

        "Region": [
            "region",
            "state",
            "country",
            "city",
        ],

        "Order Date": [
            "order date",
            "date",
            "invoice date",
        ],

        "Ship Date": [
            "ship date",
            "delivery date",
        ],

        "Order ID": [
            "order id",
            "invoice id",
            "transaction id",
        ],

    }

    # -----------------------------------------------------

    def detect(
        self,
        columns: list[str],
    ) -> list[str]:

        detected = []

        normalized = {

            column: re.sub(
                r"[_\-\s]+",
                " ",
                column.lower(),
            )

            for column in columns

        }

        for business_name, aliases in self.COLUMN_PATTERNS.items():

            for column, normalized_name in normalized.items():

                if any(

                    alias == normalized_name

                    for alias in aliases

                ):

                    detected.append(

                        f"{business_name} → {column}"

                    )

                    break

        return detected


business_column_detector = BusinessColumnDetector()