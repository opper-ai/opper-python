from typing import Any, Optional, Tuple

from opperai.embeddings.async_embeddings import AsyncEmbeddings
from opperai.embeddings.embeddings import Embeddings
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
        self.embeddings: Embeddings = Embeddings(client)
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
        self.embeddings: AsyncEmbeddings = AsyncEmbeddings(client)
        self.call = self.functions.call
