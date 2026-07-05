"""
backend/prompts/insight_prompt.py

Enterprise Prompt Builder for the AI Business
Intelligence Platform.

This module is responsible ONLY for building
prompts for Large Language Models.

Business logic must never exist here.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from textwrap import dedent

from backend.models.analysis_models import (
    AnalysisMetadata,
    AnomalyResult,
    RecommendationResult,
    SummaryResult,
    TrendResult,
)


class InsightPromptBuilder:
    """
    Enterprise Prompt Builder.

    Converts structured business analysis into
    prompts for LLMs.

    Supported LLMs

    • Gemini
    • GPT
    • Claude
    • Local LLM
    """

    @staticmethod
    def build_explanation_prompt(
        *,
        metadata: AnalysisMetadata,
        trend: TrendResult,
        anomaly: AnomalyResult,
        recommendation: RecommendationResult,
        summary: SummaryResult,
    ) -> str:
        """
        Build the executive report prompt.
        """

        recommendation_text = "\n".join(
            f"- {item.recommendation}"
            for item in recommendation.recommendations
        )

        return dedent(
            f"""
You are a Senior Business Intelligence Consultant.

Your task is to generate a professional executive report.

Never invent numbers.

Never invent statistics.

Use ONLY the provided analysis.

====================================================
BUSINESS QUESTION
====================================================

{metadata.question}

====================================================
DATASET INFORMATION
====================================================

Rows: {metadata.total_rows}

Columns: {metadata.total_columns}

Metric: {metadata.selected_metric}

Category: {metadata.selected_category}

Datetime: {metadata.selected_datetime}

====================================================
EXECUTIVE OVERVIEW
====================================================

{summary.overview}

====================================================
TREND ANALYSIS
====================================================

Trend

{trend.trend.value}

Percentage Change

{trend.percentage_change:.2f} %

First Value

{trend.first_value}

Last Value

{trend.last_value}

Trend Description

{trend.message}

====================================================
ANOMALY ANALYSIS
====================================================

{anomaly.message}

Total Anomalies

{anomaly.anomaly_count}

====================================================
BUSINESS RECOMMENDATIONS
====================================================

{recommendation_text}

====================================================
OUTPUT FORMAT
====================================================

Generate a professional business report using
the following sections.

1. Executive Summary

2. Business Overview

3. Trend Analysis

4. Anomaly Analysis

5. Risks

6. Opportunities

7. Recommendations

8. Final Conclusion

Requirements

• Professional language

• Executive style

• Clear paragraphs

• No markdown tables

• No SQL

• No fabricated insights

• Keep the report concise.

"""
        ).strip()


insight_prompt_builder = InsightPromptBuilder()