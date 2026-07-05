"""
backend/agents/agent_manager.py

Enterprise Agent Manager

Coordinates the complete AI
Business Intelligence pipeline.

Pipeline
--------
Question
    │
    ▼
PlannerAgent
    │
    ▼
SQLAgent
    │
    ▼
SQLValidator
    │
    ▼
QueryExecutor
    │
    ▼
AnalysisService
    │
    ▼
AgentResponse

Author:
Sanket Kabariya
"""

from __future__ import annotations
import pandas as pd
import logging
from dataclasses import dataclass
from typing import Optional

from backend.agents.planner_agent import (
    planner_agent,
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

from backend.services.analysis_service import (
    analysis_service,
    AnalysisServiceResponse,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Final Response
# ==========================================================

@dataclass(slots=True)
class AgentResponse:
    """
    Final response returned by Agent Manager.
    """

    success: bool

    question: str

    sql: str

    query_result: Optional[pd.DataFrame]

    analysis: Optional[
        AnalysisServiceResponse
    ]

    error: Optional[str] = None


# ==========================================================
# Agent Manager
# ==========================================================

class AgentManager:
    """
    Enterprise AI Coordinator.

    Coordinates all backend agents.

    Contains NO business logic.
    """

    def process(
        self,
        *,
        question: str,
    ) -> AgentResponse:

        logger.info(
            "Starting AI pipeline."
        )

        try:

            # ---------------------------------
            # Step 1
            # Planner
            # ---------------------------------

            plan = planner_agent.analyze(
                question
            )

            logger.info(
                "Planning completed."
            )

            # ---------------------------------
            # Step 2
            # SQL Generation
            # ---------------------------------

            sql_result = (
                sql_agent.generate_sql(
                    plan=plan
                )
            )

            if not sql_result.success:

                logger.error(
                    "SQL generation failed: %s",
                    sql_result.error,
                )

                return AgentResponse(
                    success=False,
                    question=question,
                    sql="",
                    query_result=None,
                    analysis=None,
                    error=sql_result.error,
                )

            sql = sql_result.sql

            logger.info(
                "SQL generated successfully."
            )

            #
            # Continue in Part 2
            #
            
                        # ---------------------------------
            # Step 3
            # SQL Validation
            # ---------------------------------

            validation = sql_validator.validate(
                sql=sql,
            )

            if not validation.valid:

                logger.error(
                    "SQL validation failed: %s",
                    validation.message,
                )

                return AgentResponse(
                    success=False,
                    question=question,
                    sql="",
                    query_result=None,
                    analysis=None,
                    error=validation.message,
                )

            logger.info(
                "SQL validation completed."
            )

            # ---------------------------------
            # Step 4
            # Execute SQL
            # ---------------------------------

            query_result = query_executor.execute(
                sql=sql,
            )

            if not query_result["success"]:

                logger.error(
                    "Query execution failed."
                )

                return AgentResponse(
                    success=False,
                    question=question,
                    sql="",
                    query_result=None,
                    analysis=None,
                    error=query_result.get("error", "Query execution failed."),
                )

            dataframe = query_result["data"]

            logger.info(
                "SQL executed successfully."
            )

            # ---------------------------------
            # Step 5
            # Business Analysis
            # ---------------------------------

            analysis = analysis_service.analyze(
                dataframe=dataframe,
                question=question,
            )

            if not analysis.success:

                logger.error(
                    "Analysis Service failed: %s",
                    analysis.error,
                )

                return AgentResponse(
                    success=False,
                    question=question,
                    sql="",
                    query_result=None,
                    analysis=None,
                    error=analysis.error,
                )

            logger.info(
                "Business analysis completed."
            )

            # ---------------------------------
            # Step 6
            # Final Response
            # ---------------------------------

            return AgentResponse(
                success=True,
                question=question,
                sql=sql,
                query_result=dataframe,
                analysis=analysis,
                error=None,
            )

        except Exception as error:

            logger.exception("Agent Manager failed.")

            print("=" * 80)
            print("AGENT MANAGER ERROR")
            print(type(error).__name__)
            print(str(error))
            print("=" * 80)

            return AgentResponse(
                success=False,
                question=question,
                sql="",
                query_result=None,
                analysis=None,
                error=str(error),
            )


# ==========================================================
# Singleton
# ==========================================================

agent_manager = AgentManager()