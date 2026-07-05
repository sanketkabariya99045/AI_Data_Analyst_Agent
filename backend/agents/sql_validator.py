"""
SQL Validator

Validates SQL before execution.

Project:
AI Data Analyst
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import sqlglot
from sqlglot import exp

from backend.database.schema import schema_manager


@dataclass
class ValidationResult:
    """
    SQL validation result.
    """

    valid: bool

    message: str

    tables: List[str]

    query_type: str


class SQLValidator:
    """
    Production SQL Validator.
    """

    ALLOWED = (
        exp.Select,
    )

    def validate(
        self,
        sql: str,
    ) -> ValidationResult:
        """
        Validate SQL.
        """

        try:

            tree = sqlglot.parse_one(sql)

        except Exception as error:

            return ValidationResult(
                False,
                f"SQL Parse Error: {error}",
                [],
                "UNKNOWN",
            )

        if not isinstance(tree, self.ALLOWED):

            return ValidationResult(
                False,
                "Only SELECT statements are allowed.",
                [],
                tree.key,
            )

        tables = []

        for table in tree.find_all(exp.Table):

            tables.append(table.name)

        existing = schema_manager.list_tables()

        for table in tables:

            if table not in existing:

                return ValidationResult(
                    False,
                    f"Unknown table: {table}",
                    tables,
                    tree.key,
                )

        return ValidationResult(
            True,
            "SQL is valid.",
            tables,
            tree.key,
        )


sql_validator = SQLValidator()