"""
Conversation Memory

Stores previous conversation turns.

Project:
AI Business Intelligence Platform

Author:
Sanket Kabariya
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ==========================================================
# Conversation Turn
# ==========================================================

@dataclass(slots=True)
class ConversationTurn:

    question: str

    sql: str

    chart_type: Optional[str] = None

    result_columns: List[str] = field(default_factory=list)


# ==========================================================
# Conversation Memory
# ==========================================================

class ConversationMemory:

    def __init__(self):

        self.history: List[
            ConversationTurn
        ] = []

    # ------------------------------------------

    def add(
        self,
        *,
        question: str,
        sql: str,
        chart_type: str | None = None,
        result_columns: List[str] | None = None,
    ) -> None:

        self.history.append(

            ConversationTurn(

                question=question,

                sql=sql,

                chart_type=chart_type,

                result_columns=result_columns or [],
            )
        )

    # ------------------------------------------

    def last(self) -> Optional[ConversationTurn]:

        if not self.history:

            return None

        return self.history[-1]

    # ------------------------------------------

    def clear(self):

        self.history.clear()


conversation_memory = ConversationMemory()