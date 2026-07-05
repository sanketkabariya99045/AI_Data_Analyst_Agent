"""
Database Manager

Provides high-level database operations for DuckDB.

Project: AI Data Analyst
"""

from typing import List

import duckdb
import pandas as pd

from backend.database.connection import database_connection


class DatabaseManager:
    """
    High-level interface for all DuckDB operations.
    """

    def __init__(self):
        self.connection = database_connection.get_connection()

    # ----------------------------------------------------
    # TABLE OPERATIONS
    # ----------------------------------------------------

    def create_table_from_dataframe(
        self,
        table_name: str,
        dataframe: pd.DataFrame,
        replace: bool = True
    ) -> None:
        """
        Create a DuckDB table from a Pandas DataFrame.
        """

        if replace:
            self.connection.register("temp_df", dataframe)

            self.connection.execute(
                f"""
                CREATE OR REPLACE TABLE {table_name}
                AS
                SELECT *
                FROM temp_df
                """
            )

        else:
            self.connection.register("temp_df", dataframe)

            self.connection.execute(
                f"""
                CREATE TABLE {table_name}
                AS
                SELECT *
                FROM temp_df
                """
            )

    def drop_table(self, table_name: str) -> None:
        """
        Delete a table.
        """

        self.connection.execute(
            f"DROP TABLE IF EXISTS {table_name}"
        )

    def table_exists(self, table_name: str) -> bool:
        """
        Check whether table exists.
        """

        result = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = ?
            """,
            [table_name]
        ).fetchone()

        return result[0] > 0

    def list_tables(self) -> List[str]:
        """
        Return all database tables.
        """

        result = self.connection.execute(
            """
            SHOW TABLES
            """
        ).fetchall()

        return [row[0] for row in result]

    # ----------------------------------------------------
    # QUERY OPERATIONS
    # ----------------------------------------------------

    def execute_query(
        self,
        sql: str
    ) -> pd.DataFrame:
        """
        Execute SQL and return DataFrame.
        """

        return self.connection.execute(sql).fetchdf()

    def execute_non_query(
        self,
        sql: str
    ) -> None:
        """
        Execute SQL that does not return rows.
        """

        self.connection.execute(sql)

    # ----------------------------------------------------
    # DATABASE INFORMATION
    # ----------------------------------------------------

    def get_table_row_count(
        self,
        table_name: str
    ) -> int:

        result = self.connection.execute(
            f"""
            SELECT COUNT(*)
            FROM {table_name}
            """
        ).fetchone()

        return result[0]

    def close(self):

        database_connection.close_connection()


database_manager = DatabaseManager()