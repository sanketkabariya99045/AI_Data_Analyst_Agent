"""
Dashboard Plan Adapter

Converts AI-generated dashboard plans
into DashboardPlan models.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from backend.dashboard.dashboard_models import (
    DashboardPlan,
    DashboardWidget,
    WidgetType,
)


class DashboardPlanAdapter:

    def convert(
        self,
        ai_plan: dict,
    ) -> DashboardPlan:

        widgets = []

        for widget in ai_plan.get(
            "widgets",
            [],
        ):

            widgets.append(

                DashboardWidget(

                    id=widget["id"],

                    title=widget["title"],

                    question=widget["question"],

                    widget_type=WidgetType[
                        widget["type"].upper()
                    ],

                )

            )

        return DashboardPlan(

            title=ai_plan.get(
                "title",
                "AI Dashboard",
            ),

            description=ai_plan.get(
                "description",
                "",
            ),

            widgets=widgets,

        )


dashboard_plan_adapter = DashboardPlanAdapter()