# ruff: noqa: F401
from opperai.async_functions import AsyncFunctions
from opperai.async_indexes import AsyncIndexes
from opperai.async_spans import AsyncSpans
from opperai.core.functions.decorator._decorator import fn, get_last_span_id
from opperai.core.spans._decorator import start_span, trace
from opperai.functions import Functions
from opperai.indexes import Indexes
from opperai.spans import Spans

from ._client import AsyncClient, Client


class Opper:
    client: Client = None

    functions: Functions = None
    indexes: Indexes = None
    spans: Spans = None

    def __init__(self, client: Client = None):
        if client is not None:
            if not isinstance(client, Client):
                raise ValueError("Client must be an instance of Client")
        if client is None:
            client = Client()

        self.client = client
        self.functions = Functions(client)
        self.indexes = Indexes(client)
        self.spans = Spans(client)


class AsyncOpper(Opper):
    client: AsyncClient = None

    functions: AsyncFunctions = None
    indexes: AsyncIndexes = None
    spans: AsyncSpans = None

    def __init__(self, client: AsyncClient = None):
        if client is not None:
            if not isinstance(client, AsyncClient):
                raise ValueError("Client must be an instance of AsyncClient")
        if client is None:
            client = AsyncClient()

        self.client = client
        self.functions = AsyncFunctions(client)
        self.indexes = AsyncIndexes(client)
        self.spans = AsyncSpans(client)
