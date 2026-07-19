"""
backend/services/sql_execution_service.py

Enterprise SQL Execution Service.

Central orchestration service for converting
a natural language question into SQL results.

Pipeline
--------
Question
    │
    ▼
Planner Agent
    │
    ▼
SQL Agent
    │
    ▼
SQL Validator
    │
    ▼
DuckDB Executor

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from backend.agents.planner_agent import (
    planner_agent,
    ExecutionPlan,
)

from backend.agents.sql_agent import (
    sql_agent,
)

from backend.agents.sql_validator import (
    sql_validator,
)

from backend.database.query_executor import (
    query_executor,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Response
# ==========================================================

@dataclass(slots=True)
class SQLExecutionResponse:
    """
    Final SQL execution response.
    """

    success: bool

    question: str

    plan: Optional[ExecutionPlan]

    sql: str

    dataframe: Optional[pd.DataFrame]

    execution_time: float

    error: str | None = None


# ==========================================================
# Service
# ==========================================================

class SQLExecutionService:
    """
    Enterprise SQL Execution Service.

    Responsibilities
    ----------------

    • Analyze question

    • Generate SQL

    • Validate SQL

    • Execute SQL

    Returns DataFrame only.
    """

    def execute(
        self,
        question: str,
    ) -> SQLExecutionResponse:

        logger.info(
            "Executing SQL pipeline."
        )

        try:

            # ------------------------------------------
            # Planner
            # ------------------------------------------

            plan = planner_agent.analyze(
                question,
            )

            # ------------------------------------------
            # SQL Generation
            # ------------------------------------------

            sql_result = sql_agent.generate_sql(
                plan,
            )

            if not sql_result.success:

                return SQLExecutionResponse(

                    success=False,

                    question=question,

                    plan=plan,

                    sql="",

                    dataframe=None,

                    execution_time=0,

                    error=sql_result.error,

                )

            # ------------------------------------------
            # SQL Validation
            # ------------------------------------------

            validation = sql_validator.validate(
                sql_result.sql,
            )

            if not validation.valid:

                return SQLExecutionResponse(

                    success=False,

                    question=question,

                    plan=plan,

                    sql=sql_result.sql,

                    dataframe=None,

                    execution_time=0,

                    error=validation.message,

                )

            # ------------------------------------------
            # Execute SQL
            # ------------------------------------------

            result = query_executor.execute(
                sql_result.sql,
            )

            return SQLExecutionResponse(

                success=True,

                question=question,

                plan=plan,

                sql=sql_result.sql,

                dataframe=result["data"],

                execution_time=result[
                    "execution_time"
                ],

            )

        except Exception as error:

            logger.exception(
                "SQL execution failed."
            )

            return SQLExecutionResponse(

                success=False,

                question=question,

                plan=None,

                sql="",

                dataframe=None,

                execution_time=0,

                error=str(error),

            )


# ==========================================================
# Singleton
# ==========================================================

sql_execution_service = SQLExecutionService()