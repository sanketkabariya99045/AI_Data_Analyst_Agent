"""
Dashboard SQL Models

Author:
Sanket Kabariya
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WidgetSQL:

    widget_id: str

    sql: str


@dataclass
class DashboardSQLPlan:

    widgets: list[WidgetSQL]
    def get_sql(
        self,
        widget_id: str,
    ) -> str | None:

        for widget in self.widgets:

            if widget.widget_id == widget_id:

                return widget.sql

        return None