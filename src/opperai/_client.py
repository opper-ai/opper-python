import httpx
from ._functions import Functions, AsyncFunctions
from httpx_sse import aconnect_sse, connect_sse
import json

DEFAULT_API_URL = "https://api.opper.ai"

Timeout = httpx.Timeout(60.0)


class AsyncClient:
    def __init__(self, api_key: str, api_url: str = DEFAULT_API_URL):
        self.http_client = _async_http_client(api_key, api_url)
        self.functions = AsyncFunctions(self.http_client)


class Client:
    def __init__(self, api_key: str, api_url: str = DEFAULT_API_URL):
        self.http_client = _http_client(api_key, api_url)
        self.functions = Functions(self.http_client)


class _async_http_client:
    def __init__(self, api_key: str, api_url):
        self.session = httpx.AsyncClient(
            base_url=api_url,
            headers={"X-OPPER-API-KEY": f"{api_key}"},
            timeout=Timeout,
        )

    async def do_request(self, method: str, path: str, retries: int = 3, **kwargs):
        for attempt in range(retries):
            response = await self.session.request(method, path, **kwargs)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 500:
                if attempt < retries - 1:
                    continue
                else:
                    raise Exception("Max retries reached for 500 error")
            else:
                raise Exception(f"Request failed with status {response.status_code}")

    async def stream(self, method: str, path: str):
        with aconnect_sse(
            self.session,
            method,
            path,
        ) as event_source:
            for sse in event_source.iter_sse():
                yield json.loads(sse.data)


class _http_client:
    def __init__(self, api_key: str, api_url: str):
        self.session = httpx.Client(
            base_url=api_url,
            headers={"X-OPPER-API-KEY": f"{api_key}"},
            timeout=Timeout,
        )

    def do_request(self, method: str, path: str, retries: int = 3, **kwargs):
        for attempt in range(retries):
            response = self.session.request(method, path, **kwargs)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 500:
                if attempt < retries - 1:
                    continue
                else:
                    raise Exception("Max retries reached for 500 error")
            else:
                raise Exception(f"Request failed with status {response.status_code}")

    def stream(self, method: str, path: str, **kwargs):
        with connect_sse(
            self.session,
            method,
            path,
            **kwargs,
        ) as event_source:
            for sse in event_source.iter_sse():
                yield json.loads(sse.data)
