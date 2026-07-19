"""
Prompt Builder

Creates enterprise-quality prompts
for SQL generation.

Project:
AI Data Analyst
Author:
Sanket Kabariya
"""

from typing import Dict


class PromptBuilder:
    """
    Builds enterprise SQL prompts.
    """

    SYSTEM_PROMPT = """
You are an expert SQL Data Analyst and Business Intelligence Engineer.

Generate ONLY valid DuckDB SQL.

==================================================
GENERAL RULES
==================================================

1. Return ONLY executable SQL.
2. Never explain your answer.
3. Never use markdown.
4. Never use SQL comments.
5. Never generate UPDATE.
6. Never generate DELETE.
7. Never generate INSERT.
8. Never generate CREATE.
9. Never generate DROP.
10. Never generate ALTER.
11. Use ONLY tables and columns from the schema.
12. Never invent tables.
13. Never invent column names.
14. Preserve column names EXACTLY as shown.
15. If a column contains spaces, wrap it in double quotes.

Example:

Correct:
"Customer Name"

Wrong:
Customer_Name

Wrong:
customer_name

==================================================
DUCKDB RULES
==================================================

Generate valid DuckDB SQL.

Always alias aggregated columns.

Always GROUP BY correctly.

Always ORDER BY aggregated values.

Always LIMIT Top N queries.

==================================================
DATE RULES
==================================================

If a column is VARCHAR or TEXT containing dates,
convert it ONCE using STRPTIME().

Correct:

DATE_TRUNC(
'month',
STRPTIME("Order Date", '%d/%m/%Y')
)

If the column is already DATE or TIMESTAMP,
DO NOT call STRPTIME().

Correct:

DATE_TRUNC(
'month',
"Order Date"
)

Never write:

STRPTIME(
DATE_TRUNC(...),
'%d/%m/%Y'
)

Never nest STRPTIME().

Infer the correct date format from sample rows.

==================================================
BUSINESS ANALYTICS
==================================================

Total
→ SUM()

Average
→ AVG()

Maximum
→ MAX()

Minimum
→ MIN()

Count
→ COUNT()

Distinct Count
→ COUNT(DISTINCT ...)

Top
→ ORDER BY DESC LIMIT

Bottom
→ ORDER BY ASC LIMIT

Trend
→ DATE_TRUNC()

Growth
→ Compare aggregated values by time.

==================================================
VISUALIZATION
==================================================

Generate SQL suitable for charts.

Return dimensions first.

Return measures second.

Example:

SELECT
Region,
SUM(Sales) AS TotalSales
FROM sheet1
GROUP BY Region
ORDER BY TotalSales DESC;

==================================================
WHEN DATA DOES NOT EXIST
==================================================

If the requested information is unavailable,
return:

SELECT
'Requested information is unavailable in this dataset.' AS message;
"""

    def build_sql_prompt(
        self,
        question: str,
        schema: Dict,
        dataset_profile: Dict | None = None,
    ) -> str:

        schema_text = self.format_schema(schema)

        profile_text = ""

        if dataset_profile:

            profile_text = f"""
==================================================
DATASET PROFILE
==================================================

Rows:
{dataset_profile["rows"]}

Columns:
{dataset_profile["columns"]}

Numeric Columns:
{", ".join(dataset_profile["numeric_columns"])}

Categorical Columns:
{", ".join(dataset_profile["categorical_columns"])}

Datetime Columns:
{", ".join(dataset_profile["datetime_columns"])}
"""

        prompt = f"""
{self.SYSTEM_PROMPT}

==================================================
DATABASE SCHEMA
==================================================

{schema_text}

{profile_text}

==================================================
USER QUESTION
==================================================

{question}

==================================================
OUTPUT
==================================================

Return ONLY executable DuckDB SQL.
"""

        return prompt

    def format_schema(
        self,
        schema: Dict,
    ) -> str:

        lines = []

        for table_name, table_info in schema.items():

            lines.append("=" * 60)
            lines.append(f"TABLE: {table_name}")
            lines.append("=" * 60)

            lines.append(
                f"Rows : {table_info['rows']}"
            )

            lines.append("")
            lines.append("Columns:")

            for column in table_info["columns"]:

                nullable = (
                    "NULL"
                    if column["nullable"]
                    else "NOT NULL"
                )

                column_name = column["column_name"]

                if " " in column_name:
                    column_name = f'"{column_name}"'

                lines.append(
                    f"  • {column_name} ({column['data_type']}, {nullable})"
                )

            lines.append("")

            sample_rows = table_info.get(
                "sample_rows",
                [],
            )

            if sample_rows:

                lines.append("Sample Rows:")

                for i, row in enumerate(
                    sample_rows,
                    start=1,
                ):

                    lines.append(f"Row {i}")

                    for key, value in row.items():

                        if " " in key:
                            key = f'"{key}"'

                        lines.append(
                            f"    {key}: {value}"
                        )

                    lines.append("")

            lines.append("")

        return "\n".join(lines)


prompt_builder = PromptBuilder()