"""
Dashboard Detector

Detects whether the user's request
is asking for a dashboard.

Project:
AI Business Intelligence Platform
"""

from __future__ import annotations


class DashboardDetector:

    KEYWORDS = [

        "dashboard",

        "executive dashboard",

        "analytics dashboard",

        "sales dashboard",

        "marketing dashboard",

        "finance dashboard",

        "ipl dashboard",

        "hr dashboard",

        "build dashboard",

        "create dashboard",

        "generate dashboard",

        "show dashboard",

    ]

    def is_dashboard_request(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        return any(

            keyword in question

            for keyword in self.KEYWORDS

        )


dashboard_detector = DashboardDetector()