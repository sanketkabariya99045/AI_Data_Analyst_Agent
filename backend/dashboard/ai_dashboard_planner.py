"""
AI Dashboard Planner

Creates dashboard widgets dynamically
based on the uploaded dataset.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import json
import logging

from backend.database.schema import schema_manager
from backend.llm.llm_factory import LLMFactory

logger = logging.getLogger(__name__)


class AIDashboardPlanner:

    def __init__(self):

        self.llm = LLMFactory.create(
            provider="gemini",
        )
        
    def plan(self):

        schema = schema_manager.get_database_schema()

        schema_text = []

        for table, info in schema.items():

            schema_text.append(f"TABLE: {table}")

            schema_text.append("Columns:")

            for column in info["columns"]:

                schema_text.append(
                    f'- {column["column_name"]} ({column["data_type"]})'
                )

            schema_text.append("")

            schema_text.append("Sample Rows:")

            for row in info["sample_rows"]:

                schema_text.append(str(row))

            schema_text.append("")
            
        prompt = f"""
            You are a Senior Business Intelligence Consultant.

            Your job is to design the BEST executive dashboard
            for the uploaded dataset.

            Analyze ONLY the provided schema.

            Choose the most meaningful:

            - 4 KPI widgets
            - 3 Chart widgets
            - 1 Table widget

            Return ONLY valid JSON.

            The JSON MUST follow EXACTLY this format:

            {{
                "title":"Dashboard Title",

                "description":"Short dashboard description",

                "widgets":[

                    {{
                        "id":"kpi_1",
                        "type":"KPI",
                        "title":"Total Sales",
                        "question":"Calculate total sales."
                    }},

                    {{
                        "id":"kpi_2",
                        "type":"KPI",
                        "title":"Total Customers",
                        "question":"Count total customers."
                    }},

                    {{
                        "id":"chart_1",
                        "type":"CHART",
                        "title":"Monthly Sales Trend",
                        "question":"Show monthly sales trend."
                    }},

                    {{
                        "id":"chart_2",
                        "type":"CHART",
                        "title":"Sales by Region",
                        "question":"Show total sales by region."
                    }},

                    {{
                        "id":"table_1",
                        "type":"TABLE",
                        "title":"Top Customers",
                        "question":"Show top 10 customers by sales."
                    }}

                ]
            }}

            Rules

            1. Use ONLY existing columns.
            2. Never invent columns.
            3. Never assume Profit exists.
            4. Never assume Sales exists.
            5. If the dataset is HR, create HR widgets.
            6. If the dataset is Cricket, create Cricket widgets.
            7. If the dataset is Banking, create Banking widgets.
            8. If the dataset is generic, create meaningful generic widgets.
            9. Questions must be clear because another AI will generate SQL from them.

            Database Schema

            {chr(10).join(schema_text)}
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
        return json.loads(response)
    
ai_dashboard_planner = AIDashboardPlanner()