from typing import Any, Dict, List, Optional, Tuple

from opperai.evaluations._base import BaseEvaluator, Evaluation
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
        client: Optional[Tuple[Client, Any]] = None,
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
        client: Optional[Tuple[AsyncClient, Any]] = None,
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
    context: Dict[str, Any],
    evaluator: Optional[BaseEvaluator] = None,
    evaluators: Optional[List[BaseEvaluator]] = None,
) -> Evaluation:
    from opperai.evaluations._evaluation import Evaluator

    if evaluator is not None:
        return await Evaluator([evaluator]).evaluate(span_id, context)
    else:
        return await Evaluator(evaluators).evaluate(span_id, context)
