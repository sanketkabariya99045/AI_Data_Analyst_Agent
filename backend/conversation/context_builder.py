"""
Context Builder

Builds conversational context for
follow-up questions.

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

from backend.conversation.conversation_memory import (
    conversation_memory,
)


class ContextBuilder:
    """
    Combines previous conversation
    with the current question.
    """

    def build(
        self,
        question: str,
    ) -> str:
        """
        Build prompt context.
        """

        previous = conversation_memory.last()

        if previous is None:

            return question

        context = f"""
Previous Question:
{previous.question}

Previous SQL:
{previous.sql}

Current Question:
{question}

If the current question modifies the previous analysis,
generate SQL based on the previous context.

If it is unrelated,
ignore the previous context.
"""

        return context.strip()


context_builder = ContextBuilder()