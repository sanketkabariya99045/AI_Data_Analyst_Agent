"""
Database Connection Manager

This module is responsible for creating and managing
the DuckDB database connection.

Author: Sanket
Project: AI Data Analyst
"""

from pathlib import Path
from typing import Optional

import duckdb


class DatabaseConnection:
    """
    Singleton Database Connection Manager.

    Ensures only one DuckDB connection is used
    throughout the application.
    """

    _instance = None
    _connection: Optional[duckdb.DuckDBPyConnection] = None

    DATABASE_FOLDER = Path("data")
    DATABASE_NAME = "ai_data_analyst.duckdb"

    def __new__(cls):
        """
        Create only one instance of DatabaseConnection.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def connect(self) -> duckdb.DuckDBPyConnection:
        """
        Create or return an existing DuckDB connection.
        """

        if self._connection is None:

            self.DATABASE_FOLDER.mkdir(
                parents=True,
                exist_ok=True
            )

            database_path = (
                self.DATABASE_FOLDER /
                self.DATABASE_NAME
            )

            self._connection = duckdb.connect(
                str(database_path)
            )

        return self._connection

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """
        Return active database connection.
        """

        return self.connect()

    def close_connection(self):
        """
        Close database connection safely.
        """

        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def is_connected(self) -> bool:
        """
        Check whether database connection exists.
        """

        return self._connection is not None


# Singleton instance
database_connection = DatabaseConnection()