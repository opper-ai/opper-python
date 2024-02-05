import os
from typing import Optional

from pydantic import BaseModel, Field

from ._http_clients import _async_http_client, _http_client
from .functions._async_functions import AsyncFunctions
from .functions._functions import Functions
from .indexes._async_indexes import AsyncIndexes
from .indexes._indexes import Indexes

DEFAULT_API_URL = "https://api.opper.ai"


class AsyncClient:
    _instance = None

    def __new__(cls, api_key: str = None, api_url: str = None, timeout: int = 60):
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
            cls._instance.http_client = _async_http_client(api_key, api_url, timeout)
            cls._instance.functions = AsyncFunctions(cls._instance.http_client)
            cls._instance.indexes = AsyncIndexes(cls._instance.http_client)
            cls._instance.api_key = api_key
            cls._instance.api_url = api_url
        return cls._instance


class Client:
    _instance = None

    def __new__(cls, api_key: str = None, api_url: str = None, timeout: int = 60):
        if api_key is None:
            api_key = os.getenv("OPPER_API_KEY")
            if api_key is None:
                raise Exception(
                    "API key is not provided and OPPER_API_KEY environment variable is not set."
                )
        if api_url is None:
            api_url = os.getenv("OPPER_API_URL", DEFAULT_API_URL)
        if cls._instance is None:
            instance = super(Client, cls).__new__(cls)
            instance.http_client = _http_client(api_key, api_url, timeout)
            instance.functions = Functions(instance.http_client)
            instance.indexes = Indexes(instance.http_client)
            instance.api_key = api_key
            instance.api_url = api_url
            cls._instance = instance
        return cls._instance
