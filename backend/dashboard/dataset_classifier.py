"""
Dataset Classifier

Identifies the type of uploaded dataset
based on its schema.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from backend.database.schema import schema_manager


class DatasetClassifier:

    def classify(self) -> str:

        schema = schema_manager.get_database_schema()

        columns = []

        for table in schema.values():

            for column in table["columns"]:

                columns.append(
                    column["column_name"].lower()
                )

        columns = set(columns)

        # -----------------------------
        # Sales
        # -----------------------------

        if {

            "sales",

            "customer id",

            "order date",

        }.issubset(columns):

            return "sales"

        # -----------------------------
        # HR
        # -----------------------------

        if {

            "employee",

            "salary",

            "department",

        }.issubset(columns):

            return "hr"

        # -----------------------------
        # Banking
        # -----------------------------

        if {

            "balance",

            "loan",

        }.issubset(columns):

            return "bank"

        # -----------------------------
        # Cricket
        # -----------------------------

        if (

            "batter" in columns

            or "bowler" in columns

            or "runs" in columns

        ):

            return "cricket"

        # -----------------------------
        # Generic
        # -----------------------------

        return "generic"


dataset_classifier = DatasetClassifier()