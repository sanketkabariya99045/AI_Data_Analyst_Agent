"""
Prompt Builder

Creates production-quality prompts
for SQL generation.

Project:
AI Data Analyst
"""

from typing import Dict


class PromptBuilder:
    """
    Builds prompts for the SQL Agent.
    """

    SYSTEM_PROMPT = """
You are an expert SQL Data Analyst.

Your task is to generate accurate DuckDB SQL queries.

Rules:

1. Generate ONLY SQL.
2. Never explain your answer.
3. Never use markdown.
4. Never generate UPDATE.
5. Never generate DELETE.
6. Never generate DROP.
7. Never generate INSERT.
8. Never generate ALTER.
9. Use only tables and columns from the schema.
10. If information is unavailable, return a SQL comment explaining why.
"""

    def build_sql_prompt(
        self,
        question: str,
        schema: Dict
    ) -> str:
        """
        Build SQL generation prompt.
        """

        schema_text = self.format_schema(schema)

        prompt = f"""
{self.SYSTEM_PROMPT}

========================================
DATABASE SCHEMA
========================================

{schema_text}

========================================
USER QUESTION
========================================

{question}

========================================
OUTPUT
========================================

Return ONLY valid DuckDB SQL.
"""

        return prompt

    def format_schema(
        self,
        schema: Dict
    ) -> str:
        """
        Convert schema dictionary into readable text.
        """

        lines = []

        for table_name, table_info in schema.items():

            lines.append(f"TABLE: {table_name}")

            for column in table_info["columns"]:

                lines.append(
                    f"  - {column['column_name']} ({column['data_type']})"
                )

            lines.append("")

        return "\n".join(lines)


prompt_builder = PromptBuilder()