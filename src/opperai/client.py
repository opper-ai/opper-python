import httpx
from .functions import Functions, AsyncFunctions

DEFAULT_API_URL = "https://api.opper.ai"


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
            base_url=api_url, headers={"X-OPPER-API-KEY": f"{api_key}"}
        )

    async def do_request(self, method: str, path: str, **kwargs):
        response = await self.session.request(method, path, **kwargs)
        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}")
        return response.json()


class _http_client:
    def __init__(self, api_key: str, api_url: str):
        self.session = httpx.Client(
            base_url=api_url, headers={"X-OPPER-API-KEY": f"{api_key}"}
        )

    def do_request(self, method: str, path: str, **kwargs):
        response = self.session.request(method, path, **kwargs)
        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}")
        return response.json()
