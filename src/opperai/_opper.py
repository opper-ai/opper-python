import inspect
import json
from typing import Any, Dict, List, Optional

from opperai.embeddings.async_embeddings import AsyncEmbeddings
from opperai.embeddings.embeddings import Embeddings
from opperai.evaluations._base import Evaluation
from opperai.functions.async_functions import AsyncFunctions
from opperai.functions.functions import Functions
from opperai.indexes.async_indexes import AsyncIndexes
from opperai.indexes.indexes import Indexes
from opperai.spans.async_spans import AsyncSpans
from opperai.spans.spans import Spans

from ._client import AsyncClient, Client
from .core.utils import prepare_input

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
        self.embeddings: Embeddings = Embeddings(client)
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
        self.embeddings: AsyncEmbeddings = AsyncEmbeddings(client)
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

    opper = AsyncOpper()
    # Get span for saving metrics
    span = opper.spans.get_span(span_id=span_id)

    # Run each evaluator and process the metrics
    for evaluator_result, kwargs in evaluators:
        async with opper.spans.start(
            name=evaluator_result.__name__,
            parent_span_id=span.uuid,
            type="evaluation",
        ) as evaluation_span:
            # Check if result is a coroutine and await it if needed
            if inspect.iscoroutine(evaluator_result):
                print("evaluator_result is a coroutine")
                metrics = await evaluator_result
            elif callable(evaluator_result):
                print("evaluator_result is a callable")
                metrics = evaluator_result()
                # Check if the callable returned a coroutine
                if inspect.iscoroutine(metrics):
                    print("metrics is a coroutine")
                    metrics = await metrics
            else:
                print("evaluator_result is not a coroutine or callable")
                metrics = evaluator_result

            # Ensure we have a list of metrics
            if not isinstance(metrics, list):
                metrics = [metrics]

            # Validate that each metric has a dimension
            for i, metric in enumerate(metrics):
                if not metric.dimension:
                    raise ValueError(f"Metric at index {i} must have a dimension")

            # Save metrics directly to span
            for metric in metrics:
                await span.save_metric(
                    dimension=metric.dimension,
                    value=metric.value or 0.0,
                    comment=metric.comment or "",
                )

            # Add metrics to flat list
            if "metrics" not in all_metrics:
                all_metrics["metrics"] = []
            all_metrics["metrics"].extend(metrics)

            if isinstance(kwargs, str):
                await evaluation_span.update(
                    input=kwargs, output=json.dumps(prepare_input(metrics))
                )
            else:
                await evaluation_span.update(
                    input=json.dumps(prepare_input(kwargs)),
                    output=json.dumps(prepare_input(metrics)),
                )

    # Create the final evaluation
    return Evaluation(metrics=all_metrics)
