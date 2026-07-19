"""
Follow-up Detector

Determines whether a user's question is
a follow-up to the previous question.

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

import re


class FollowUpDetector:
    """
    Detects conversational follow-up questions.
    """

    FOLLOWUP_KEYWORDS = {

        # Filters
        "only",
        "where",
        "exclude",
        "include",
        "greater",
        "less",
        "above",
        "below",
        "between",

        # Ranking
        "top",
        "bottom",
        "highest",
        "lowest",
        "first",
        "last",

        # Sorting
        "ascending",
        "descending",
        "sort",
        "order",

        # Chart changes
        "pie",
        "bar",
        "line",
        "scatter",
        "histogram",
        "chart",
        "graph",

        # Time
        "today",
        "yesterday",
        "month",
        "year",
        "quarter",
        "week",

        # Comparison
        "compare",
        "versus",
        "vs",

        # Add / Remove
        "also",
        "instead",
        "remove",
        "add",
        "replace",

        # Reference words
        "this",
        "that",
        "same",
        "previous",
        "again",
    }

    SHORT_QUESTION_LIMIT = 6

    # -------------------------------------------------

    def is_followup(
        self,
        question: str,
    ) -> bool:
        """
        Returns True if the question is likely
        a follow-up.
        """

        text = question.lower().strip()

        words = re.findall(r"\w+", text)

        # Very short questions are usually follow-ups
        if len(words) <= self.SHORT_QUESTION_LIMIT:
            return True

        # Contains follow-up keywords
        if any(
            keyword in text
            for keyword in self.FOLLOWUP_KEYWORDS
        ):
            return True

        return False


followup_detector = FollowUpDetector()