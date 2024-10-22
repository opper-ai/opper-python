import json
from http import HTTPStatus

import httpx
from httpx_sse import aconnect_sse, connect_sse
from opperai.__version__ import __version__
from opperai.types import Errors
from opperai.types.exceptions import (
    ContentPolicyViolationError,
    ContextWindowExceededError,
    NotFoundError,
    OpperAPIError,
    OpperTimeoutError,
    RateLimitError,
    RequestValidationError,
    StructuredGenerationError,
)


def _raise_error(response: httpx.Response):
    error = Errors.model_validate(response.json())
    error = error.errors[0]
    status_code = response.status_code

    if status_code == HTTPStatus.BAD_REQUEST:
        if error.type == "StructuredGenerationError":
            raise StructuredGenerationError(error.message, error.detail)
        if error.type == "ContentPolicyViolationError":
            raise ContentPolicyViolationError(error.message, error.detail)
        if error.type == "ContextWindowExceededError":
            raise ContextWindowExceededError(error.message, error.detail)
    if status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        if error.type == "RequestValidationError":
            raise RequestValidationError(error.message, error.detail)
    if status_code == HTTPStatus.TOO_MANY_REQUESTS:
        if error.type == "RateLimitError":
            raise RateLimitError(error.message, error.detail)
    if status_code == HTTPStatus.NOT_FOUND:
        raise NotFoundError(error.message, error.detail)
    else:
        raise OpperAPIError(error.message, error.detail)


class _async_http_client:
    def __init__(self, api_key: str, api_url: str, timeout: float):
        self.session = httpx.AsyncClient(
            base_url=api_url,
            headers={
                "X-OPPER-API-KEY": f"{api_key}",
                "User-Agent": f"opper-python/{__version__}",
            },
            timeout=httpx.Timeout(timeout),
        )

    async def do_request(self, method: str, path: str, **kwargs):
        try:
            response = await self.session.request(method, path, **kwargs)
            if response.status_code >= 400:
                _raise_error(response)
            return response
        except httpx.TimeoutException as e:
            raise OpperTimeoutError(
                "request timed out",
                "The request to the opper api timed out.",
            ) from e

    async def stream(self, method: str, path: str, **kwargs):
        try:
            async with aconnect_sse(
                self.session,
                method,
                path,
                **kwargs,
            ) as event_source:
                response = event_source.response
                if response.status_code >= 400:
                    await response.aread()
                    _raise_error(response)

                async for sse in event_source.aiter_sse():
                    yield json.loads(sse.data)
        except httpx.TimeoutException as e:
            raise OpperTimeoutError(
                "request timed out",
                "The request to the opper api timed out.",
            ) from e


class _http_client:
    def __init__(self, api_key: str, api_url: str, timeout):
        self.session = httpx.Client(
            base_url=api_url,
            headers={
                "X-OPPER-API-KEY": f"{api_key}",
                "User-Agent": f"opper-python/{__version__}",
            },
            timeout=httpx.Timeout(timeout),
        )

    def do_request(self, method: str, path: str, **kwargs):
        try:
            response = self.session.request(method, path, **kwargs)
            if response.status_code >= 400:
                _raise_error(response)
            return response
        except httpx.TimeoutException as e:
            raise OpperTimeoutError(
                "request timed out",
                "The request to the opper api timed out.",
            ) from e

    def stream(self, method: str, path: str, **kwargs):
        try:
            with connect_sse(
                self.session,
                method,
                path,
                **kwargs,
            ) as event_source:
                response = event_source.response
                if response.status_code >= 400:
                    response.read()
                    _raise_error(response)

                for sse in event_source.iter_sse():
                    yield json.loads(sse.data)
        except httpx.TimeoutException as e:
            raise OpperTimeoutError(
                "request timed out",
                "the request to the opper api timed out.",
            ) from e
