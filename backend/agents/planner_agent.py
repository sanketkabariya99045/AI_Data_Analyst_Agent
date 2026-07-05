"""
Planner Agent

Analyzes a user's natural language question and creates
an execution plan for downstream agents.

Project:
AI Data Analyst
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ExecutionPlan:
    """
    Structured execution plan.
    """

    user_question: str

    intent: str

    requires_sql: bool

    requires_chart: bool

    requires_forecast: bool

    confidence: float

    entities: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)


class PlannerAgent:
    """
    Responsible for understanding the user's request.

    Later this class can be upgraded to use an LLM,
    but initially we use rule-based intent detection.
    """

    CHART_KEYWORDS = {
        "chart",
        "graph",
        "plot",
        "trend",
        "visualize",
        "line",
        "bar",
        "pie",
        "dashboard",
    }

    FORECAST_KEYWORDS = {
        "forecast",
        "predict",
        "future",
        "next month",
        "next year",
        "estimate",
    }

    SUMMARY_KEYWORDS = {
        "summary",
        "overview",
        "describe",
        "profile",
        "statistics",
    }

    def analyze(self, question: str) -> ExecutionPlan:
        """
        Analyze the user's question.
        """

        text = question.lower()

        requires_chart = any(
            word in text
            for word in self.CHART_KEYWORDS
        )

        requires_forecast = any(
            word in text
            for word in self.FORECAST_KEYWORDS
        )

        if requires_forecast:
            intent = "forecast"

        elif requires_chart:
            intent = "visualization"

        elif any(word in text for word in self.SUMMARY_KEYWORDS):
            intent = "summary"

        else:
            intent = "sql_analysis"

        requires_sql = not requires_forecast

        return ExecutionPlan(
            user_question=question,
            intent=intent,
            requires_sql=requires_sql,
            requires_chart=requires_chart,
            requires_forecast=requires_forecast,
            confidence=0.90,
            entities=self.extract_entities(question),
            metadata={},
        )

    def extract_entities(self, question: str) -> List[str]:
        """
        Placeholder entity extractor.

        Later this will be replaced with an
        LLM or NER pipeline.
        """

        tokens = []

        for word in question.split():

            cleaned = word.strip(",.?")

            if len(cleaned) > 2:

                tokens.append(cleaned)

        return tokens


planner_agent = PlannerAgent()