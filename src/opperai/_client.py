import os

from ._http_clients import _async_http_client, _http_client
from .functions._async_functions import AsyncFunctions
from .functions._functions import Functions

DEFAULT_API_URL = "https://api.opper.ai"


class AsyncClient:
    _instance = None

    def __new__(cls, api_key: str = None, api_url: str = None):
        if api_key is None:
            api_key = os.getenv("OPPER_API_KEY")
            if api_key is None:
                raise Exception(
                    "API key is not provided and OPPER_API_KEY environment variable is not set."
                )
        if api_url is None:
            api_url = os.getenv("OPPER_API_URL", DEFAULT_API_URL)
        if cls._instance is None:
            cls._instance = super(AsyncClient, cls).__new__(cls)
            cls._instance.http_client = _async_http_client(api_key, api_url)
            cls._instance.functions = AsyncFunctions(cls._instance.http_client)
        return cls._instance


class Client:
    _instance = None

    def __new__(cls, api_key: str = None, api_url: str = None):
        if api_key is None:
            api_key = os.getenv("OPPER_API_KEY")
            if api_key is None:
                raise Exception(
                    "API key is not provided and OPPER_API_KEY environment variable is not set."
                )
            if api_url is None:
                api_url = os.getenv("OPPER_API_URL", DEFAULT_API_URL)
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
            cls._instance.http_client = _http_client(api_key, api_url)
            cls._instance.functions = Functions(cls._instance.http_client)
        return cls._instance
