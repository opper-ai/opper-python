import base64
import os
from http import HTTPStatus
from typing import Any, Tuple

from opperai.core.datasets._async_datasets import AsyncDatasets as CoreAsyncDatasets
from opperai.core.datasets._datasets import Datasets as CoreDatasets
from opperai.core.functions._async_functions import AsyncFunctions as CoreAsyncFunctions
from opperai.core.functions._functions import Functions as CoreFunctions
from opperai.core.indexes._async_indexes import AsyncIndexes as CoreAsyncIndexes
from opperai.core.indexes._indexes import Indexes as CoreIndexes
from opperai.core.spans._async_spans import AsyncSpans as CoreAsyncSpans
from opperai.core.spans._spans import Spans as CoreSpans
from opperai.types import CallPayload, FunctionResponse, ImageOutput
from opperai.types.exceptions import APIError

from .core._http_clients import _async_http_client, _http_client

DEFAULT_API_URL = "https://api.opper.ai"
DEFAULT_TIMEOUT = 120


class AsyncClient:
    functions: CoreAsyncFunctions = None
    indexes: CoreAsyncIndexes = None
    spans: CoreAsyncSpans = None
    datasets: CoreAsyncDatasets = None

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
        self.functions = CoreAsyncFunctions(
            self.http_client, default_model=default_model
        )
        self.indexes = CoreAsyncIndexes(self.http_client)
        self.spans = CoreAsyncSpans(self.http_client)
        self.datasets = CoreAsyncDatasets(self.http_client)

    async def generate_image(self, prompt: str) -> Tuple[ImageOutput, None]:
        """Generate an image from a prompt.
        Note: only Azure dall-e-3 is supported.
        """
        response = await self.http_client.do_request(
            "POST",
            "/v1/generate-image",
            json={"model": "azure/dall-e-3-eu", "prompt": prompt, "format": "b64_json"},
        )

        base64_image = response.json()["result"]["base64_image"]
        image_bytes = base64.b64decode(base64_image)

        return ImageOutput(image_bytes), None

    async def call(self, payload: CallPayload) -> Any:
        response = await self.http_client.do_request(
            "POST",
            "/v1/call",
            json=payload.model_dump(),
        )

        if response.status_code == HTTPStatus.OK:
            return FunctionResponse.model_validate(response.json())

        raise APIError(
            f"Failed to run function {payload.name} with status {response.status_code}: {response.text}"
        )


class Client:
    functions: CoreFunctions
    indexes: CoreIndexes
    spans: CoreSpans
    datasets: CoreDatasets

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
        self.functions = CoreFunctions(self.http_client, default_model=default_model)
        self.indexes = CoreIndexes(self.http_client)
        self.spans = CoreSpans(self.http_client)
        self.datasets = CoreDatasets(self.http_client)

    def generate_image(self, prompt: str) -> Tuple[ImageOutput, None]:
        """Generate an image from a prompt.
        Note: only Azure dall-e-3 is supported.
        """
        response = self.http_client.do_request(
            "POST",
            "/v1/generate-image",
            json={"model": "azure/dall-e-3-eu", "prompt": prompt, "format": "b64_json"},
        )

        base64_image = response.json()["result"]["base64_image"]
        image_bytes = base64.b64decode(base64_image)

        return ImageOutput(image_bytes), None

    def call(self, payload: CallPayload) -> Any:
        response = self.http_client.do_request(
            "POST",
            "/v1/call",
            json=payload.model_dump(),
        )

        if response.status_code == HTTPStatus.OK:
            return FunctionResponse.model_validate(response.json())

        raise APIError(
            f"Failed to run function {payload.name} with status {response.status_code}: {response.text}"
        )


from opperai.functions.async_functions import AsyncFunctions
from opperai.functions.functions import Functions
from opperai.indexes.async_indexes import AsyncIndexes
from opperai.indexes.indexes import Indexes
from opperai.spans.async_spans import AsyncSpans
from opperai.spans.spans import Spans


class Opper:
    def __init__(self, client: Client = None, api_key: str = None):
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
    def __init__(self, client: AsyncClient = None, api_key: str = None):
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
