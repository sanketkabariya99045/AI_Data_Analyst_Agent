"""
Suggestion Engine

Project:
AI Business Intelligence Platform
"""

from __future__ import annotations

from backend.suggestions.question_templates import (
    QUESTION_TEMPLATES,
)

from backend.suggestions.suggestion_models import (
    SuggestedQuestion,
    SuggestionResult,
)


class SuggestionEngine:

    def generate(
        self,
        business_columns: list[str],
    ) -> SuggestionResult:

        suggestions = []

        added = set()

        for item in business_columns:

            # Sales -> Sales
            business_type = item.split("→")[0].strip()

            if business_type not in QUESTION_TEMPLATES:

                continue

            for question in QUESTION_TEMPLATES[business_type]:

                if question in added:

                    continue

                suggestions.append(

                    SuggestedQuestion(

                        question=question,

                        category=business_type,
                    )

                )

                added.add(question)

        return SuggestionResult(

            suggestions=suggestions
        )


suggestion_engine = SuggestionEngine()