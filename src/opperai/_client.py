import base64
import os
from http import HTTPStatus
from typing import Any, Tuple

from opperai.core.datasets._async_datasets import AsyncDatasets
from opperai.core.datasets._datasets import Datasets
from opperai.core.functions._async_functions import AsyncFunctions
from opperai.core.functions._functions import Functions
from opperai.core.indexes._async_indexes import AsyncIndexes
from opperai.core.indexes._indexes import Indexes
from opperai.core.spans._async_spans import AsyncSpans
from opperai.core.spans._spans import Spans
from opperai.types import CallConfiguration, CallPayload, FunctionResponse, ImageOutput
from opperai.types.exceptions import APIError

from .core._http_clients import _async_http_client, _http_client

DEFAULT_API_URL = "https://api.opper.ai"
DEFAULT_TIMEOUT = 120


class AsyncClient:
    functions: AsyncFunctions = None
    indexes: AsyncIndexes = None
    spans: AsyncSpans = None
    datasets: AsyncDatasets = None

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
        self.datasets = AsyncDatasets(self.http_client)

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
    functions: Functions
    indexes: Indexes
    spans: Spans
    datasets: Datasets

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
        self.datasets = Datasets(self.http_client)

    def generate_image(
        self, prompt: str, configuration: CallConfiguration
    ) -> Tuple[ImageOutput, None]:
        """Generate an image from a prompt.
        Note: only Azure dall-e-3 is supported.
        """
        payload = {
            "model": "azure/dall-e-3-eu",
            "prompt": prompt,
            "format": "b64_json",
            **configuration.model_parameters,
        }
        response = self.http_client.do_request(
            "POST",
            "/v1/generate-image",
            json=payload,
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
