"""
backend/dashboard/dashboard_templates.py

Enterprise Dashboard Templates.

Defines reusable dashboard blueprints.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from backend.dashboard.dashboard_models import (
    DashboardPlan,
    DashboardWidget,
    WidgetType,
)


class DashboardTemplates:
    """
    Enterprise Dashboard Templates.
    """

    # ======================================================
    # Sales Dashboard
    # ======================================================

    @staticmethod
    def sales_dashboard() -> DashboardPlan:

        return DashboardPlan(

            title="Sales Dashboard",

            description=(
                "Executive overview of sales performance."
            ),

            widgets=[

                # ============================
                # KPI Cards
                # ============================

                DashboardWidget(
                    id="total_sales",
                    title="Total Sales",
                    question="Calculate the total sales amount.",
                    widget_type=WidgetType.KPI,
                ),

                DashboardWidget(
                    id="total_profit",
                    title="Total Profit",
                    question="Calculate the total profit.",
                    widget_type=WidgetType.KPI,
                ),

                DashboardWidget(
                    id="total_orders",
                    title="Total Orders",
                    question="Count the total number of orders.",
                    widget_type=WidgetType.KPI,
                ),

                DashboardWidget(
                    id="total_customers",
                    title="Total Customers",
                    question="Count the distinct customers.",
                    widget_type=WidgetType.KPI,
                ),

                # ============================
                # Charts
                # ============================

                DashboardWidget(
                    id="sales_region",
                    title="Sales by Region",
                    question="Show total sales grouped by region.",
                    widget_type=WidgetType.CHART,
                ),

                DashboardWidget(
                    id="monthly_sales",
                    title="Monthly Sales Trend",
                    question="Show monthly total sales trend.",
                    widget_type=WidgetType.CHART,
                ),

                DashboardWidget(
                    id="category_sales",
                    title="Category Performance",
                    question="Compare total sales by category.",
                    widget_type=WidgetType.CHART,
                ),

                # ============================
                # Summary
                # ============================

                DashboardWidget(
                    id="summary",
                    title="Executive Summary",
                    question="Generate executive business insights.",
                    widget_type=WidgetType.SUMMARY,
                ),

            ],

        )

    # ======================================================
    # Finance Dashboard
    # ======================================================

    @staticmethod
    def finance_dashboard() -> DashboardPlan:

        return DashboardPlan(

            title="Finance Dashboard",

            description=(
                "Executive financial performance dashboard."
            ),

            widgets=[

                DashboardWidget(
                    id="revenue",
                    title="Revenue",
                    question="What is total revenue?",
                    widget_type=WidgetType.KPI,
                ),

                DashboardWidget(
                    id="profit",
                    title="Profit",
                    question="What is total profit?",
                    widget_type=WidgetType.KPI,
                ),

                DashboardWidget(
                    id="margin",
                    title="Profit Margin",
                    question="Calculate overall profit margin.",
                    widget_type=WidgetType.KPI,
                ),

                DashboardWidget(
                    id="monthly_profit",
                    title="Monthly Profit",
                    question="Show monthly profit trend.",
                    widget_type=WidgetType.CHART,
                ),

                DashboardWidget(
                    id="summary",
                    title="Executive Summary",
                    question="Provide financial summary.",
                    widget_type=WidgetType.SUMMARY,
                ),
            ],
        )

    # ======================================================
    # Inventory Dashboard
    # ======================================================

    @staticmethod
    def inventory_dashboard() -> DashboardPlan:

        return DashboardPlan(

            title="Inventory Dashboard",

            description=(
                "Inventory performance overview."
            ),

            widgets=[

                DashboardWidget(
                    id="products",
                    title="Total Products",
                    question="How many products are available?",
                    widget_type=WidgetType.KPI,
                ),

                DashboardWidget(
                    id="stock",
                    title="Current Stock",
                    question="Show current stock levels.",
                    widget_type=WidgetType.TABLE,
                ),

                DashboardWidget(
                    id="category_stock",
                    title="Stock by Category",
                    question="Show stock by category.",
                    widget_type=WidgetType.CHART,
                ),

                DashboardWidget(
                    id="summary",
                    title="Inventory Summary",
                    question="Provide inventory summary.",
                    widget_type=WidgetType.SUMMARY,
                ),
            ]

        )

    # ======================================================
    # HR Dashboard
    # ======================================================

    @staticmethod
    def hr_dashboard() -> DashboardPlan:

        return DashboardPlan(

            title="HR Dashboard",

            description=(
                "Human Resource analytics dashboard."
            ),

            widgets=[

                DashboardWidget(
                    id="employees",
                    title="Employees",
                    question="How many employees are there?",
                    widget_type=WidgetType.KPI,
                ),

                DashboardWidget(
                    id="department",
                    title="Department Distribution",
                    question="Show employee count by department.",
                    widget_type=WidgetType.CHART,
                ),

                DashboardWidget(
                    id="salary",
                    title="Salary Distribution",
                    question="Show salary distribution.",
                    widget_type=WidgetType.CHART,
                ),

                DashboardWidget(
                    id="summary",
                    title="HR Summary",
                    question="Provide HR executive summary.",
                    widget_type=WidgetType.SUMMARY,
                ),
            ]

        )


# ==========================================================
# Singleton
# ==========================================================

dashboard_templates = DashboardTemplates()