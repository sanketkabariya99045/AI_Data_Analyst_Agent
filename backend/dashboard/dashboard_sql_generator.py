"""
Enterprise Dashboard SQL Generator.

Generates SQL for the entire dashboard
using ONE LLM call.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import json
import logging

from backend.database.schema import (
    schema_manager,
)

from backend.llm.llm_factory import (
    LLMFactory,
)

logger = logging.getLogger(__name__)

class DashboardSQLGenerator:

    def __init__(self):

        self.llm = LLMFactory.create(
            provider="gemini",
        )
        
    def generate(
        self,
        plan,
    ):

        schema = schema_manager.get_database_schema()
        columns = set()
        schema_text = []
        
        for table_info in schema.values():

            for column in table_info["columns"]:

                columns.add(
                    column["column_name"].lower()
                )
                

        for table, info in schema.items():

            schema_text.append(f"TABLE: {table}")

            for column in info["columns"]:

                schema_text.append(
                    f'- {column["column_name"]} ({column["data_type"]})'
                )

        widgets = []

        for widget in plan.widgets:

            if widget.widget_type.name == "SUMMARY":
                continue

            # Skip Profit widget if Profit column doesn't exist
            

            widgets.append(
                {
                    "id": widget.id,
                    "type": widget.widget_type.name,
                    "title": widget.title,
                    "question": widget.question,
                }
            )
            
        prompt = f"""
        You are an expert SQL Engineer specializing in DuckDB.

        Your task is to generate ONE SQL query for EACH dashboard widget.

        DATABASE SCHEMA

        {chr(10).join(schema_text)}

        DASHBOARD WIDGETS

        {json.dumps(widgets, indent=2)}

        IMPORTANT DATE RULES

        If a date column is stored as TEXT,
        use STRPTIME().

        Infer the correct date format from the schema and sample rows.

        Examples:

        08/11/2017
        → STRPTIME("Order Date", '%d/%m/%Y')

        2017-11-08
        → STRPTIME("Order Date", '%Y-%m-%d')

        Never use:

        CAST("Order Date" AS DATE)

        on text date columns.

        RULES

        1. Generate ONE SQL query for every widget.
        2. Use ONLY columns that exist in the schema.
        3. Never invent column names.
        4. Never invent table names.
        5. KPI widgets should return a single row.
        6. Chart widgets should return grouped or aggregated data.
        7. Table widgets should return detailed records.
        8. Use valid DuckDB SQL only.
        9. Every SQL query must be executable.
        10. Do not include explanations.
        11. Return ONLY valid JSON.

        The JSON keys MUST match the widget IDs exactly.

        Example:

        {{
            "kpi_1":"SELECT SUM(Sales) AS total_sales FROM superstore",
            "kpi_2":"SELECT COUNT(DISTINCT Order_ID) AS total_orders FROM superstore",
            "chart_1":"SELECT Region, SUM(Sales) AS sales FROM superstore GROUP BY Region",
            "table_1":"SELECT Customer_Name, SUM(Sales) AS sales FROM superstore GROUP BY Customer_Name ORDER BY sales DESC LIMIT 10"
        }}
        """
            
        response = self.llm.generate(
            prompt
        )
        response = response.replace(
            "```json",
            "",
        )

        response = response.replace(
            "```",
            "",
        )

        response = response.strip()
        
        try:

            sql_map = json.loads(response)

            # --------------------------------------------
            # Clean SQL
            # --------------------------------------------

            for widget_id, sql in list(sql_map.items()):

                if sql is None:
                    continue

                sql = sql.strip()

                # Remove markdown
                sql = sql.replace("```sql", "")
                sql = sql.replace("```", "")
                sql = sql.strip()

                # Ignore comments
                if "--" in sql:
                    sql = sql.split("--")[0].strip()

                # Only allow executable SQL
                if not (
                    sql.upper().startswith("SELECT")
                    or sql.upper().startswith("WITH")
                ):
                    logger.warning(
                        "Ignoring invalid SQL for %s",
                        widget_id,
                    )
                    sql_map[widget_id] = None
                    continue

                sql_map[widget_id] = sql

            return sql_map

        except Exception:

            logger.exception(
                "Dashboard SQL generation failed."
            )

            return {}

dashboard_sql_generator = DashboardSQLGenerator()