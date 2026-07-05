"""
Loader Module

Loads Pandas DataFrames into DuckDB automatically.

Project:
AI Data Analyst
"""

from typing import Dict, List

import pandas as pd

from backend.database.database import database_manager


class DataLoader:
    """
    Responsible for loading uploaded
    DataFrames into DuckDB.
    """

    def __init__(self):

        self.database = database_manager

    # -------------------------------------------------

    def clean_table_name(
        self,
        table_name: str
    ) -> str:
        """
        Convert filename or sheet name into
        SQL-friendly table name.
        """

        table_name = table_name.lower()

        table_name = table_name.replace(" ", "_")

        table_name = table_name.replace("-", "_")

        table_name = table_name.replace(".", "_")

        return table_name

    # -------------------------------------------------

    def load_dataframe(
        self,
        dataframe: pd.DataFrame,
        table_name: str
    ) -> str:
        """
        Load one DataFrame into DuckDB.
        """

        cleaned_name = self.clean_table_name(
            table_name
        )

        self.database.create_table_from_dataframe(
            cleaned_name,
            dataframe
        )

        return cleaned_name

    # -------------------------------------------------

    def load_multiple_dataframes(
        self,
        dataframes: Dict[str, pd.DataFrame]
    ) -> List[str]:
        """
        Load multiple sheets into DuckDB.
        """

        created_tables = []

        for sheet_name, dataframe in dataframes.items():

            table = self.load_dataframe(
                dataframe,
                sheet_name
            )

            created_tables.append(table)

        return created_tables

    # -------------------------------------------------

    def load_excel_workbook(
        self,
        workbook: Dict[str, pd.DataFrame]
    ) -> List[str]:
        """
        Alias for Excel workbook loading.
        """

        return self.load_multiple_dataframes(
            workbook
        )


loader = DataLoader()