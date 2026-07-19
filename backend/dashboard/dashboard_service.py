"""
backend/dashboard/dashboard_service.py

Enterprise Dashboard Service

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging

from backend.dashboard.dashboard_models import (
    Dashboard,
    WidgetType,
)
from backend.database.query_executor import (
    query_executor,
)
from backend.dashboard.dashboard_table_engine import (
    dashboard_table_engine,
)
from backend.dashboard.dashboard_sql_generator import (
    dashboard_sql_generator,
)

from backend.services.sql_execution_service import (
    SQLExecutionResponse,
)

from backend.dashboard.ai_dashboard_planner import (
    ai_dashboard_planner,
)

from backend.dashboard.dashboard_plan_adapter import (
    dashboard_plan_adapter,
)
from backend.dashboard.dashboard_kpi_engine import (
    dashboard_kpi_engine,
)

from backend.dashboard.dashboard_chart_engine import (
    dashboard_chart_engine,
)

from backend.dashboard.dashboard_summary_engine import (
    dashboard_summary_engine,
)



logger = logging.getLogger(__name__)


class DashboardService:

    def build_dashboard(
        self,
        question: str,
    ) -> Dashboard:

        logger.info("Building Dashboard")

        # -----------------------------------
        # Build dashboard plan
        # -----------------------------------

        # -----------------------------------------
        # AI Dashboard Planning
        # -----------------------------------------

        plan_json = ai_dashboard_planner.plan()

        logger.info(
            "AI Dashboard Plan Generated."
        )

        plan = dashboard_plan_adapter.convert(
            plan_json,
        )

        logger.info(
            "Dashboard contains %d widgets.",
            len(plan.widgets),
        )
        # -----------------------------------
        # Generate ALL SQL in ONE Gemini call
        # -----------------------------------

        sql_map = dashboard_sql_generator.generate(
            plan
        )

        logger.info(
            "Generated SQL for %d widgets",
            len(sql_map),
        )
        kpi_results = []
        chart_results = []
        table_results = []

        # -----------------------------------
        # Execute Widgets
        # -----------------------------------

        for widget in plan.widgets:

            if widget.widget_type == WidgetType.SUMMARY:
                continue
            logger.info(
                "Executing widget : %s",
                widget.title,
            )

            # -----------------------------------
            # Execute widget using SQL Library
            # -----------------------------------

            try:

                sql = sql_map.get(widget.id)

                if not sql:

                    logger.warning(
                        "No SQL generated for widget: %s",
                        widget.title,
                    )

                    continue

                query_result = query_executor.execute(sql)

                result = SQLExecutionResponse(

                    success=query_result["success"],

                    question=widget.question,

                    plan=None,

                    sql=sql,

                    dataframe=query_result["data"],

                    execution_time=query_result["execution_time"],

                    error=None,

                )

            except Exception as error:

                logger.exception(
                    "Widget failed : %s",
                    widget.title,
                )

                continue

            if not result.success:

                logger.warning(
                    "Widget failed : %s",
                    widget.title,
                )

                continue

            if widget.widget_type == WidgetType.KPI:

                kpi_results.append(result)

            elif widget.widget_type == WidgetType.CHART:

                chart_results.append(result)

            elif widget.widget_type == WidgetType.TABLE:

                table_results.append(result)


        # -----------------------------------
        # Build Dashboard Components
        # -----------------------------------

        kpis = dashboard_kpi_engine.build(
            kpi_results
        )

        charts = dashboard_chart_engine.build(
            chart_results
        )
        
        tables = dashboard_table_engine.build(
            table_results
        )
        
        summary = dashboard_summary_engine.generate(

            title=plan.title,

            kpis=kpis,

            charts=charts,

        )

        successful = (
            len(kpi_results)
            + len(chart_results)
            + len(table_results)
        )

        failed = (
            len(plan.widgets)
            - successful
        )

        return Dashboard(

            title=plan.title,

            description=plan.description,

            kpis=kpis,

            charts=charts,
            
            tables=tables,
            
            summary=summary,
            
            metadata={

                "widgets": len(plan.widgets),

                "successful_queries": successful,

                "failed_queries": failed,

            },

        )


dashboard_service = DashboardService()