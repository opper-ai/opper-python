import os

from opperai.core.functions._async_functions import AsyncFunctions
from opperai.core.functions._functions import Functions
from opperai.core.indexes._async_indexes import AsyncIndexes
from opperai.core.indexes._indexes import Indexes
from opperai.core.spans._async_spans import AsyncSpans
from opperai.core.spans._spans import Spans

from .core._http_clients import _async_http_client, _http_client

DEFAULT_API_URL = "https://api.opper.ai"
DEFAULT_TIMEOUT = 120


class AsyncClient:
    functions: AsyncFunctions = None
    indexes: AsyncIndexes = None
    spans: AsyncSpans = None

    def __init__(
        self,
        api_key: str = None,
        api_url: str = None,
        default_model: str = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        if api_key is None:
            api_key = os.getenv("OPPER_API_KEY")
            if api_key is None:
                raise Exception(
                    "API key is not provided and OPPER_API_KEY environment variable is not set."
                )
        if api_url is None:
            api_url = os.getenv("OPPER_API_URL", DEFAULT_API_URL)
        if default_model is None:
            default_model = os.getenv("OPPER_DEFAULT_MODEL")

        self.api_key = api_key
        self.api_url = api_url
        self.default_model = default_model

        self.http_client = _async_http_client(api_key, api_url, timeout)
        self.functions = AsyncFunctions(self.http_client, default_model=default_model)
        self.indexes = AsyncIndexes(self.http_client)
        self.spans = AsyncSpans(self.http_client)


class Client:
    functions: Functions
    indexes: Indexes
    spans: Spans

    def __init__(
        self,
        api_key: str = None,
        api_url: str = None,
        default_model: str = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        if api_key is None:
            api_key = os.getenv("OPPER_API_KEY")
            if api_key is None:
                raise Exception(
                    "API key is not provided and OPPER_API_KEY environment variable is not set."
                )
        if api_url is None:
            api_url = os.getenv("OPPER_API_URL", DEFAULT_API_URL)
        if default_model is None:
            default_model = os.getenv("OPPER_DEFAULT_MODEL")

        self.api_key = api_key
        self.api_url = api_url
        self.default_model = default_model

        self.http_client = _http_client(api_key, api_url, timeout)
        self.functions = Functions(self.http_client, default_model=default_model)
        self.indexes = Indexes(self.http_client)
        self.spans = Spans(self.http_client)
