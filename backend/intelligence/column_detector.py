"""
backend/intelligence/column_detector.py

Enterprise Business Column Detector.

Detects important business columns from any dataset.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from typing import Dict

from backend.intelligence.constants import COLUMN_KEYWORDS


class ColumnDetector:
    """
    Detect business-related columns.

    Example
    -------
    Input:
        [
            "Sales",
            "Profit",
            "Customer ID",
            "Order Date",
        ]

    Output:
        {
            "sales": "Sales",
            "profit": "Profit",
            "customer": "Customer ID",
            "date": "Order Date",
        }
    """

    @staticmethod
    def detect(
        columns: list[str],
    ) -> Dict[str, str]:
        """
        Detect business columns using a scoring system.
        """

        detected: Dict[str, str] = {}

        for business_type, keywords in COLUMN_KEYWORDS.items():

            best_column = None
            best_score = -1

            for column in columns:

                normalized = column.lower().strip()

                score = 0

                for keyword in keywords:

                    # Exact match
                    if normalized == keyword:
                        score += 100

                    # Ends with keyword (TotalSales, NetProfit)
                    elif normalized.endswith(keyword):
                        score += 80

                    # Starts with keyword
                    elif normalized.startswith(keyword):
                        score += 60

                    # Contains keyword
                    elif keyword in normalized:
                        score += 40

                # Penalize date/grouping columns
                if any(
                    token in normalized
                    for token in [
                        "month",
                        "year",
                        "quarter",
                        "week",
                        "day",
                    ]
                ):
                    score -= 100

                if score > best_score:

                    best_score = score
                    best_column = column

            if best_column and best_score > 0:

                detected[business_type] = best_column

        return detected


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

column_detector = ColumnDetector()