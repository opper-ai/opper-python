import json

import httpx
from httpx_sse import aconnect_sse, connect_sse
from opperai.types.exceptions import OpperTimeoutError


class _async_http_client:
    def __init__(self, api_key: str, api_url: str, timeout: float):
        self.session = httpx.AsyncClient(
            base_url=api_url,
            headers={"X-OPPER-API-KEY": f"{api_key}"},
            timeout=httpx.Timeout(timeout),
        )

    async def do_request(self, method: str, path: str, **kwargs):
        try:
            return await self.session.request(method, path, **kwargs)
        except httpx.TimeoutException as e:
            raise OpperTimeoutError("request timed out") from e

    async def stream(self, method: str, path: str, **kwargs):
        try:
            async with aconnect_sse(
                self.session,
                method,
                path,
                **kwargs,
            ) as event_source:
                async for sse in event_source.aiter_sse():
                    yield json.loads(sse.data)
        except httpx.TimeoutException as e:
            raise OpperTimeoutError("request timed out") from e


class _http_client:
    def __init__(self, api_key: str, api_url: str, timeout):
        self.session = httpx.Client(
            base_url=api_url,
            headers={"X-OPPER-API-KEY": f"{api_key}"},
            timeout=httpx.Timeout(timeout),
        )

    def do_request(self, method: str, path: str, **kwargs):
        try:
            return self.session.request(method, path, **kwargs)
        except httpx.TimeoutException as e:
            raise OpperTimeoutError("request timed out") from e

    def stream(self, method: str, path: str, **kwargs):
        try:
            with connect_sse(
                self.session,
                method,
                path,
                **kwargs,
            ) as event_source:
                for sse in event_source.iter_sse():
                    yield json.loads(sse.data)
        except httpx.TimeoutException as e:
            raise OpperTimeoutError("request timed out") from e
