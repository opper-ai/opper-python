from typing import Any, Dict, List

from pydantic import BaseModel, Field

from opperai.types import Metric


class Evaluation(BaseModel):
    """Results of an evaluation."""

    # Map of evaluator name to metrics
    metrics: Dict[str, List[Metric]] = Field(default_factory=dict)


class BaseEvaluator:
    """Base class for evaluators."""

    def __init__(self, name: str):
        self.name = name

    async def evaluate(self, context: Dict[str, Any], **kwargs) -> Evaluation:
        """Evaluate the context and return success, score, and metrics.

        Args:
            context: Dictionary containing the result, span_id, and other context.
            **kwargs: Additional keyword arguments.

        Returns:
            Tuple containing:
                - success: Boolean indicating if the evaluation passed
                - score: Float score from 0.0 to 1.0
                - metrics: List of SpanMetric objects
        """
        raise NotImplementedError("Subclasses must implement evaluate")
