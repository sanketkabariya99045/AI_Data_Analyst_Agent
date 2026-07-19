"""
Schema Manager

Reads schema information from DuckDB.

Project:
AI Data Analyst
"""

from typing import Dict, List

from backend.database.database import database_manager


class SchemaManager:
    """
    Responsible for reading
    DuckDB schema information.
    """

    def __init__(self):

        self.database = database_manager

    # ---------------------------------------------

    def list_tables(self) -> List[str]:
        """
        Return all database tables.
        """

        return self.database.list_tables()

    # ---------------------------------------------

    def table_exists(
        self,
        table_name: str
    ) -> bool:

        return self.database.table_exists(
            table_name
        )

    # ---------------------------------------------

    def get_table_schema(
        self,
        table_name: str
    ) -> List[Dict]:
        """
        Return schema for one table.
        """

        query = f"""
        DESCRIBE {table_name}
        """

        df = self.database.execute_query(query)

        schema = []

        for _, row in df.iterrows():

            schema.append({

                "column_name": row["column_name"],

                "data_type": row["column_type"],

                "nullable": row["null"]
            })

        return schema

    # ---------------------------------------------

    def get_column_names(
        self,
        table_name: str
    ) -> List[str]:

        schema = self.get_table_schema(
            table_name
        )

        return [

            column["column_name"]

            for column in schema
        ]

    # ---------------------------------------------

    def get_table_info(
        self,
        table_name: str
    ) -> Dict:
        """
        Complete information for one table.
        """

        return {

            "table_name": table_name,

            "rows":
            self.database.get_table_row_count(
                table_name
            ),

            "columns":
            self.get_table_schema(
                table_name
            ),

            "sample_rows":
            self.get_sample_rows(
                table_name
            )
        }
        # ---------------------------------------------

    def get_sample_rows(
        self,
        table_name: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Return sample rows from the table.
        """

        query = f"""
        SELECT *
        FROM {table_name}
        LIMIT {limit}
        """

        df = self.database.execute_query(query)

        return df.to_dict(
            orient="records"
        )
    # ---------------------------------------------

    def get_database_schema(self) -> Dict:
        """
        Return complete database schema.
        """

        database_schema = {}

        tables = self.list_tables()

        for table in tables:

            database_schema[table] = (

                self.get_table_info(table)

            )

        return database_schema


schema_manager = SchemaManager()