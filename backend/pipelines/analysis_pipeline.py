"""
backend/pipelines/analysis_pipeline.py

Enterprise Analysis Pipeline.

Wraps the existing AI analysis workflow
inside the reusable Pipeline framework.

Author:
Sanket Kabariya
"""

from __future__ import annotations

from backend.core.context import (
    PipelineContext,
)

from backend.core.pipeline import (
    Pipeline,
)

from backend.stages.planner_stage import (
    PlannerStage,
)

from backend.stages.sql_generation_stage import (
    SQLGenerationStage,
)

from backend.stages.sql_validation_stage import (
    SQLValidationStage,
)

from backend.stages.sql_execution_stage import (
    SQLExecutionStage,
)

from backend.stages.analysis_stage import (
    AnalysisStage,
)

from backend.stages.chart_stage import (
    ChartStage,
)


class AnalysisPipeline:
    """
    Enterprise Analysis Pipeline.
    """

    def __init__(self):

        self.pipeline = Pipeline()

        self.pipeline.add_stage(
            PlannerStage(),
        )

        self.pipeline.add_stage(
            SQLGenerationStage(),
        )

        self.pipeline.add_stage(
            SQLValidationStage(),
        )

        self.pipeline.add_stage(
            SQLExecutionStage(),
        )

        self.pipeline.add_stage(
            AnalysisStage(),
        )

        self.pipeline.add_stage(
            ChartStage(),
        )

    # --------------------------------------------------

    def run(
        self,
        question: str,
    ):

        context = PipelineContext(
            question=question,
        )

        return self.pipeline.run(
            context,
        )


# ==========================================================
# Singleton
# ==========================================================

analysis_pipeline = AnalysisPipeline()