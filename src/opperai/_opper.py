import inspect
from typing import Any, Dict, List, Optional

from opperai.evaluations._base import Evaluation
from opperai.evaluations.decorator import process_metrics
from opperai.functions.async_functions import AsyncFunctions
from opperai.functions.functions import Functions
from opperai.indexes.async_indexes import AsyncIndexes
from opperai.indexes.indexes import Indexes
from opperai.spans.async_spans import AsyncSpans
from opperai.spans.spans import Spans

from ._client import AsyncClient, Client

DEFAULT_API_URL = "https://api.opper.ai"
DEFAULT_TIMEOUT = 120


class Opper:
    def __init__(
        self,
        client: Optional[Client] = None,
        api_key: Optional[str] = None,
    ):
        if client is not None:
            if not isinstance(client, Client):
                raise ValueError("Client must be an instance of Client")
        if api_key is not None:
            client = Client(api_key=api_key)
        if client is None:
            client = Client()

        self.client: Client = client
        self.functions: Functions = Functions(client)
        self.indexes: Indexes = Indexes(client)
        self.spans: Spans = Spans(client)  # deprecated
        self.traces: Spans = self.spans
        self.call = self.functions.call


class AsyncOpper(Opper):
    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        api_key: Optional[str] = None,
    ):
        if client is not None:
            if not isinstance(client, AsyncClient):
                raise ValueError("Client must be an instance of AsyncClient")
        if api_key is not None:
            client = AsyncClient(api_key=api_key)
        if client is None:
            client = AsyncClient()

        self.client: AsyncClient = client
        self.functions: AsyncFunctions = AsyncFunctions(client)
        self.indexes: AsyncIndexes = AsyncIndexes(client)
        self.spans: AsyncSpans = AsyncSpans(client)  # deprecated
        self.traces: AsyncSpans = self.spans
        self.call = self.functions.call
        self.evaluate = _evaluate


async def _evaluate(
    span_id: str,
    context: Optional[Dict[str, Any]] = None,
    evaluators: Optional[List[Any]] = None,
) -> Evaluation:
    """Evaluate a span using the provided evaluator functions.

    Args:
        span_id: The ID of the span to evaluate
        context: Dictionary containing result and other context
        evaluators: A list of evaluator functions or metrics

    Returns:
        Evaluation result
    """
    # Create default context if not provided
    if context is None:
        context = {}

    # Ensure span_id is in the context
    context["span_id"] = span_id

    if not evaluators:
        # No evaluators provided
        return Evaluation(metrics={})

    # Store all metrics
    all_metrics = {}

    # Run each evaluator and process the metrics
    for i, evaluator_result in enumerate(evaluators):
        # Check if result is a coroutine and await it if needed
        if inspect.iscoroutine(evaluator_result):
            metrics = await evaluator_result
        elif callable(evaluator_result):
            metrics = evaluator_result()
            # Check if the callable returned a coroutine
            if inspect.iscoroutine(metrics):
                metrics = await metrics
        else:
            metrics = evaluator_result

        # Get a name for this evaluator result
        metric_group = None
        if (
            metrics
            and len(metrics) > 0
            and hasattr(metrics[0], "dimension")
            and metrics[0].dimension
        ):
            metric_group = (
                metrics[0].dimension.split(".")[0]
                if "." in metrics[0].dimension
                else metrics[0].dimension
            )
        else:
            # Fallback if no dimension is available
            metric_group = f"evaluator_{i}"

        # Process the metrics
        eval_result = await process_metrics(metric_group, metrics)

        # Update all metrics
        all_metrics.update(eval_result.metrics)

    # Create the final evaluation
    return Evaluation(metrics=all_metrics)
