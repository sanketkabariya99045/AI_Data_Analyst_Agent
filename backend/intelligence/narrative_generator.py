"""
Enterprise Narrative Generator.

Creates executive-level business summaries
from KPIs and insights.
"""

from __future__ import annotations


class NarrativeGenerator:

    def generate(
        self,
        kpis,
        insights,
    ) -> str:

        lines = []

        if kpis:

            lines.append(
                "Key business metrics were successfully calculated."
            )

        for insight in insights[:3]:

            lines.append(
                insight.description
            )

        lines.append(
            "Overall business performance appears stable."
        )

        return " ".join(lines)


narrative_generator = NarrativeGenerator()