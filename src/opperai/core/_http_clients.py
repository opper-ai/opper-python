import json

import httpx
from httpx_sse import aconnect_sse, connect_sse


class _async_http_client:
    def __init__(self, api_key: str, api_url, timeout):
        self.session = httpx.AsyncClient(
            base_url=api_url,
            headers={"X-OPPER-API-KEY": f"{api_key}"},
            timeout=httpx.Timeout(timeout),
        )

    async def do_request(self, method: str, path: str, **kwargs):
        return await self.session.request(method, path, **kwargs)

    async def stream(self, method: str, path: str, **kwargs):
        async with aconnect_sse(self.session, method, path, **kwargs) as event_source:
            async for sse in event_source.aiter_sse():
                yield json.loads(sse.data)


class _http_client:
    def __init__(self, api_key: str, api_url: str, timeout):
        self.session = httpx.Client(
            base_url=api_url,
            headers={"X-OPPER-API-KEY": f"{api_key}"},
            timeout=httpx.Timeout(timeout),
        )

    def do_request(self, method: str, path: str, **kwargs):
        return self.session.request(method, path, **kwargs)

    def stream(self, method: str, path: str, **kwargs):
        with connect_sse(
            self.session,
            method,
            path,
            **kwargs,
        ) as event_source:
            for sse in event_source.iter_sse():
                yield json.loads(sse.data)
