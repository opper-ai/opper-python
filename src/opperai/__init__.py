# ruff: noqa: F401
from opperai.core.spans._decorator import start_span, trace
from opperai.functions.async_functions import AsyncFunctions
from opperai.functions.decorator._decorator import fn, get_last_span_id
from opperai.functions.functions import Functions
from opperai.indexes.async_indexes import AsyncIndexes
from opperai.indexes.indexes import Index, Indexes
from opperai.spans.async_spans import AsyncSpans
from opperai.spans.spans import Spans

from .__version__ import __version__
from ._client import AsyncClient, Client


class Opper:
    client: Client = None

    def __init__(self, client: Client = None):
        if client is not None:
            if not isinstance(client, Client):
                raise ValueError("Client must be an instance of Client")
        if client is None:
            client = Client()

        self.client: Client = client
        self.functions: Functions = Functions(client)
        self.indexes: Indexes = Indexes(client)
        self.spans: Spans = Spans(client)  # deprecated
        self.traces: Spans = self.spans
        self.call = self.functions.call


class AsyncOpper(Opper):
    client: AsyncClient = None

    def __init__(self, client: AsyncClient = None):
        if client is not None:
            if not isinstance(client, AsyncClient):
                raise ValueError("Client must be an instance of AsyncClient")
        if client is None:
            client = AsyncClient()

        self.client: AsyncClient = client
        self.functions: AsyncFunctions = AsyncFunctions(client)
        self.indexes: AsyncIndexes = AsyncIndexes(client)
        self.spans: AsyncSpans = AsyncSpans(client)  # deprecated
        self.traces: AsyncSpans = self.spans
        self.call = self.functions.call
