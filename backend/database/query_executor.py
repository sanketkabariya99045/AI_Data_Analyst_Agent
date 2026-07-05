"""
Query Executor

Safely executes SQL queries on DuckDB.

Project:
AI Data Analyst
"""

import time
from typing import Dict

import pandas as pd

from backend.database.database import database_manager


class QueryExecutor:
    """
    Executes SQL safely.
    """

    BLOCKED_KEYWORDS = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
    ]

    def __init__(self):

        self.database = database_manager

    # ------------------------------------------

    def validate_sql(
        self,
        sql: str
    ) -> None:
        """
        Validate SQL before execution.
        """

        sql_upper = sql.upper()

        for keyword in self.BLOCKED_KEYWORDS:

            if keyword in sql_upper:

                raise ValueError(
                    f"Blocked SQL keyword detected: {keyword}"
                )

        if not sql_upper.strip().startswith("SELECT"):

            raise ValueError(
                "Only SELECT statements are allowed."
            )

    # ------------------------------------------

    def execute(
        self,
        sql: str
    ) -> Dict:
        """
        Execute SQL safely.
        """

        self.validate_sql(sql)

        start = time.perf_counter()

        dataframe = self.database.execute_query(sql)

        end = time.perf_counter()

        return {

            "success": True,

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "execution_time": round(
                end - start,
                4
            ),

            "data": dataframe
        }

    # ------------------------------------------

    def preview_table(
        self,
        table_name: str,
        limit: int = 10
    ) -> Dict:
        """
        Preview first rows of a table.
        """

        sql = f"""

        SELECT *

        FROM {table_name}

        LIMIT {limit}

        """

        return self.execute(sql)

    # ------------------------------------------

    def count_rows(
        self,
        table_name: str
    ) -> int:
        """
        Return total rows.
        """

        sql = f"""

        SELECT COUNT(*) AS total

        FROM {table_name}

        """

        result = self.execute(sql)

        return int(

            result["data"]

            ["total"]

            .iloc[0]

        )


query_executor = QueryExecutor()