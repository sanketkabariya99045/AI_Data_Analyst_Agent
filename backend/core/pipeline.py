"""
backend/core/pipeline.py

Enterprise Pipeline Engine.

Reusable orchestration engine.

Author:
Sanket Kabariya
"""

from __future__ import annotations

import logging
import time

from backend.core.context import (
    PipelineContext,
)

from backend.core.result import (
    PipelineResult,
)

from backend.core.stage import (
    PipelineStage,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Pipeline
# ==========================================================

class Pipeline:
    """
    Enterprise Pipeline Engine.

    Responsibilities
    ----------------

    • Execute stages

    • Measure execution time

    • Handle failures

    • Return PipelineResult
    """

    def __init__(self) -> None:

        self._stages: list[
            PipelineStage
        ] = []

    # ------------------------------------------------------

    def add_stage(
        self,
        stage: PipelineStage,
    ) -> None:
        """
        Register a pipeline stage.
        """

        self._stages.append(
            stage,
        )

    # ------------------------------------------------------

    @property
    def stages(self):

        return self._stages

    # ------------------------------------------------------

    def run(
        self,
        context: PipelineContext,
    ) -> PipelineResult:

        logger.info(
            "Pipeline started."
        )

        start = time.perf_counter()

        completed = 0

        try:

            for stage in self._stages:

                logger.info(
                    "Executing stage: %s",
                    stage.name,
                )

                context = stage.run(
                    context,
                )

                completed += 1

                if context.error:

                    logger.error(
                        "Pipeline stopped at stage: %s",
                        stage.name,
                    )

                    break

            end = time.perf_counter()

            return PipelineResult(

                success=context.error is None,

                context=context,

                execution_time=round(
                    end - start,
                    3,
                ),

                stages_completed=completed,

                warnings=context.warnings,

                metadata=context.metadata,

                error=context.error,

            )

        except Exception as error:

            logger.exception(
                "Pipeline failed."
            )

            end = time.perf_counter()

            context.error = str(
                error,
            )

            return PipelineResult(

                success=False,

                context=context,

                execution_time=round(
                    end - start,
                    3,
                ),

                stages_completed=completed,

                warnings=context.warnings,

                metadata=context.metadata,

                error=str(error),

            )