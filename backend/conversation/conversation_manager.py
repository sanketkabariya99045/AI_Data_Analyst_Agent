"""
Conversation Manager

Coordinates conversation memory,
follow-up detection, and context building.

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

from backend.conversation.context_builder import (
    context_builder,
)

from backend.conversation.conversation_memory import (
    conversation_memory,
)

from backend.conversation.followup_detector import (
    followup_detector,
)


class ConversationManager:
    """
    Enterprise Conversation Manager.
    """

    # -----------------------------------------------------

    def prepare_question(
        self,
        question: str,
    ) -> str:
        """
        Build context-aware question.
        """

        if followup_detector.is_followup(
            question
        ):

            return context_builder.build(
                question
            )

        return question

    # -----------------------------------------------------

    def remember(
        self,
        *,
        question: str,
        sql: str,
        chart_type: str | None = None,
        result_columns: list[str] | None = None,
    ) -> None:
        """
        Store conversation turn.
        """

        conversation_memory.add(

            question=question,

            sql=sql,

            chart_type=chart_type,

            result_columns=result_columns,
        )

    # -----------------------------------------------------

    def clear(self) -> None:
        """
        Clear conversation.
        """

        conversation_memory.clear()


conversation_manager = ConversationManager()