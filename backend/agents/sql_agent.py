"""
SQL Agent

Responsible for generating SQL from
natural language.

Project:
AI Data Analyst
"""

from __future__ import annotations

import re
from dataclasses import dataclass
import json
from backend.agents.planner_agent import ExecutionPlan
from backend.prompts.prompt_builder import prompt_builder
from backend.database.schema import schema_manager
from backend.llm.llm_factory import LLMFactory


@dataclass
class SQLGenerationResult:
    """
    Result returned by SQL Agent.
    """

    success: bool

    sql: str

    prompt: str

    model: str

    error: str | None = None


class SQLAgent:
    """
    AI SQL Generator.
    """

    def __init__(
        self,
        provider: str = "gemini",
    ):

        self.llm = LLMFactory.create(
            provider=provider
        )

    # -----------------------------------------------------

    def generate_sql(
        self,
        plan: ExecutionPlan,
    ) -> SQLGenerationResult:
        """
        Generate SQL from execution plan.
        """

        try:

            schema = schema_manager.get_database_schema()

            dataset_profile = {}

            try:

                tables = list(schema.keys())

                if tables:

                    table_name = tables[0]

                    sample_rows = schema[table_name].get(
                        "sample_rows",
                        [],
                    )

                    if sample_rows:

                        import pandas as pd

                        dataframe = pd.DataFrame(sample_rows)

                        from backend.database.dataset_profiler import (
                            dataset_profiler,
                        )

                        dataset_profile = dataset_profiler.profile(
                            dataframe
                        )

            except Exception:

                dataset_profile = {}

            prompt = prompt_builder.build_sql_prompt(
                question=plan.user_question,
                schema=schema,
                dataset_profile=dataset_profile,
            )

            response = self.llm.generate(prompt)

            sql = self.clean_sql(response)

            return SQLGenerationResult(
                success=True,
                sql=sql,
                prompt=prompt,
                model=self.llm.model_name,
            )

        except Exception as error:

            return SQLGenerationResult(
                success=False,
                sql="",
                prompt="",
                model=self.llm.model_name,
                error=str(error),
            )

    # -----------------------------------------------------

    @staticmethod
    def clean_sql(sql: str) -> str:
        """
        Remove markdown formatting from LLM output.
        """

        sql = sql.strip()

        sql = re.sub(
            r"```sql",
            "",
            sql,
            flags=re.IGNORECASE,
        )

        sql = sql.replace("```", "")

        return sql.strip()

    def generate_dashboard_sql(
        self,
        plan,
    ):
        questions = []

        for widget in plan.widgets:

            if widget.widget_type.name == "SUMMARY":
                continue

            questions.append(

                f"{widget.id}: {widget.question}"

            )
        prompt = f"""
            You are an expert SQL engineer.

            Generate DuckDB SQL.

            Return ONLY valid JSON.

            For each dashboard widget return SQL.

            Widgets:

            {chr(10).join(questions)}

            Schema:

            {schema_text}

            Return JSON like

            {{
            "widget_id":"SELECT ..."
            }}
            """
        response = self.llm.generate(
            prompt,
        )
        sql_map = json.loads(response)
        return sql_map
    
sql_agent = SQLAgent()