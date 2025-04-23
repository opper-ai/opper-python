from typing import Any, Dict, List, Optional

from opperai._opper import AsyncOpper
from opperai.evaluations._base import BaseEvaluator, Evaluation
from opperai.types.spans import SpanMetric


class Evaluator(BaseEvaluator):
    """Class for running evaluations on Opper API calls."""

    def __init__(self, evaluators: Optional[List[BaseEvaluator]] = None):
        """Initialize with optional list of evaluators.

        Args:
            evaluators: Optional list of Evaluator instances
        """
        self.evaluators = evaluators or []
        self._opper = AsyncOpper()

    def add_evaluator(self, evaluator: BaseEvaluator):
        """Add an evaluator to the evaluation.

        Args:
            evaluator: Evaluator instance to add

        Returns:
            Self for method chaining
        """
        self.evaluators.append(evaluator)
        return self

    async def evaluate(self, span_id: str, context: Dict[str, Any]) -> Evaluation:
        """Run all evaluators on the context and save metrics to the span.

        Args:
            span_id: The span ID to attach metrics to
            context: Dictionary containing result, span_id, and other context

        Returns:
            Dictionary of metrics grouped by evaluator name
        """

        evaluation = Evaluation(
            results={},
            metrics={},
            success=False,
            score=0.0,
        )

        all_metrics = []

        # Add span_id to the context if not already present
        context["span_id"] = span_id

        # Run each evaluator
        for evaluator in self.evaluators:
            _evaluation = await evaluator.evaluate(context)
            evaluation.results[evaluator.name] = {
                "success": _evaluation.success,
                "score": _evaluation.score,
                "metrics": _evaluation.metrics,
            }
            evaluation.metrics[evaluator.name] = _evaluation.metrics[evaluator.name]
            all_metrics.extend(_evaluation.metrics[evaluator.name])

            # Save metrics to the span
            span = self._opper.spans.get_span(span_id=span_id)
            for metric in evaluation.metrics[evaluator.name]:
                await span.save_metric(
                    dimension=metric.dimension or "",
                    value=metric.value or 0.0,
                    comment=metric.comment or "",
                )

        # Calculate overall success and score
        if evaluation.results:
            evaluation.success = all(
                result["success"] for result in evaluation.results.values()
            )
            evaluation.score = sum(
                result["score"] for result in evaluation.results.values()
            ) / len(evaluation.results)

            # Create and save overall metrics
            overall_metrics = [
                SpanMetric(
                    dimension="eval.score",
                    value=evaluation.score,
                    comment="Overall evaluation score",
                ),
                SpanMetric(
                    dimension="eval.success",
                    value=1.0 if evaluation.success else 0.0,
                    comment="Overall evaluation success",
                ),
            ]

            all_metrics.extend(overall_metrics)
            evaluation.metrics["overall"] = overall_metrics

            # Save overall metrics to span
            span = self._opper.spans.get_span(span_id=span_id)
            for metric in overall_metrics:
                await span.save_metric(
                    dimension=metric.dimension or "",
                    value=metric.value or 0.0,
                    comment=metric.comment or "",
                )
        else:
            # Create default overall metrics if no evaluators were run
            evaluation.success = True
            evaluation.score = 0.0

            default_metrics = [
                SpanMetric(
                    dimension="eval.score",
                    value=0.0,
                    comment="No evaluators were run",
                ),
                SpanMetric(
                    dimension="eval.success",
                    value=1.0,
                    comment="No evaluators were run",
                ),
            ]

            all_metrics.extend(default_metrics)
            evaluation.metrics["overall"] = default_metrics

        return evaluation

    def __getattr__(self, name):
        """Get metrics by evaluator name.

        Args:
            name: Name of the evaluator

        Returns:
            Metrics for the named evaluator

        Raises:
            AttributeError: If no metrics with the given name exist
        """
        if name in self.metrics:
            return self.metrics[name]
        raise AttributeError(f"No evaluation metrics named '{name}'")

    @property
    def success(self):
        """Return whether all evaluations passed."""
        return self.overall_success if self.overall_success is not None else False

    @property
    def score(self):
        """Return the overall score."""
        return self.overall_score if self.overall_score is not None else 0.0

    def __str__(self):
        """Return a string representation of the evaluation."""
        if not self.results:
            return "No evaluations run yet."

        parts = [
            f"Overall: Success={self.overall_success}, Score={self.overall_score:.1f}"
        ]

        for name, result in self.results.items():
            metrics_str = ", ".join(
                [f"{m.dimension}={m.value}" for m in result["metrics"][:2]]
            )
            parts.append(
                f"{name}: Success={result['success']}, Score={result['score']:.1f}, {metrics_str}"
            )

        return "\n".join(parts)
