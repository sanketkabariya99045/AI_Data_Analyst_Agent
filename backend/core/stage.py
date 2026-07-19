"""
backend/core/stage.py

Enterprise Pipeline Stage.

Base class for all pipeline stages.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
import logging

from backend.core.context import PipelineContext

logger = logging.getLogger(__name__)


# ==========================================================
# Base Pipeline Stage
# ==========================================================

class PipelineStage(ABC):
    """
    Abstract base class for every pipeline stage.

    Every stage receives a PipelineContext,
    modifies it, and returns it.
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self.name = name

    # ------------------------------------------------------

    @abstractmethod
    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Execute one pipeline stage.

        Must return the updated context.
        """

        raise NotImplementedError

    # ------------------------------------------------------

    def before_execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Hook executed before the stage.
        """

        logger.info(
            "Starting stage: %s",
            self.name,
        )

    # ------------------------------------------------------

    def after_execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Hook executed after the stage.
        """

        logger.info(
            "Completed stage: %s",
            self.name,
        )

    # ------------------------------------------------------

    def run(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Execute the complete lifecycle
        of the stage.
        """

        self.before_execute(
            context,
        )

        context = self.execute(
            context,
        )

        self.after_execute(
            context,
        )

        return context