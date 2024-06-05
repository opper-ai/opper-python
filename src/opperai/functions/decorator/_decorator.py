import asyncio
import contextlib
import inspect
import json
import os
import threading
from functools import wraps
from json import JSONEncoder
from typing import List, Optional, Tuple, Union, get_args, get_origin, get_type_hints

from opperai._client import AsyncClient, Client
from opperai.core.spans import get_current_span_id
from opperai.core.utils import convert_function_call_to_json
from opperai.functions.async_functions import AsyncFunctionResponse
from opperai.functions.functions import FunctionResponse
from opperai.types import (
    CacheConfiguration,
    ChatPayload,
    FunctionIn,
    Message,
)
from pydantic import BaseModel

from ._schemas import get_output_schema

_thread_local = threading.local()


@contextlib.contextmanager
def span_id_context():
    _thread_local.span_id = None
    try:
        yield
    finally:
        del _thread_local.span_id


def get_last_span_id() -> str:
    """Retrieve the last span ID from thread-local storage."""
    return getattr(_thread_local, "span_id", None)


def _clients(
    client: Optional[Union[Client, AsyncClient]] = None,
) -> Tuple[Client, AsyncClient]:
    print("client", client.project, client.api_key, client.api_url)
    if isinstance(client, AsyncClient):
        sync_client = Client(
            api_key=client.api_key,
            api_url=client.api_url,
            project=client.project.name,
        )
        async_client = client
    elif isinstance(client, Client):
        sync_client = client
        async_client = AsyncClient(
            api_key=client.api_key,
            api_url=client.api_url,
            project=client.project.name,
        )
    else:
        async_client = AsyncClient()
        sync_client = Client()

    return sync_client, async_client


def fn(
    _func=None,
    *,
    path: Optional[str] = None,
    client: Optional[Union[Client, AsyncClient]] = None,
    json_encoder: Optional[JSONEncoder] = None,
    model: Optional[str] = None,
    few_shot: Optional[bool] = None,
    few_shot_count: Optional[int] = None,
    cache_config: Optional[CacheConfiguration] = None,
):
    """Decorator to to create a function in OpperAI's API

    This decorator can automatically handle both synchronous and asynchronous functions,
    wrapping them to perform necessary setup before invoking the OpperAI API. It allows
    for the specification of various parameters to customize the API request, including
    the use of few-shot learning, caching, and custom JSON encoding.

    Parameters:
    - path (str, optional): The API path for the function. Defaults to the decorated function's name.
    - client (Client or AsyncClient, optional): The OpperAI client instance to use. If not provided, a new instance is created.
    - json_encoder (JSONEncoder, optional): Custom JSON encoder for serializing the request payload.
    - model (str, optional): The model to use for the request. If not provided, defaults to the environment's default model.
    - few_shot (bool, optional): Whether to enable few-shot learning. Defaults to False or the environment setting.
    - few_shot_count (int, optional): The number of few-shot examples to use. Only relevant if few_shot is True.
    - cache_config (CacheConfiguration, optional): Configuration for caching API responses.

    Returns:
    - A decorated function that, when called, sets up the necessary OpperAI function and invokes the API, handling both synchronous and asynchronous execution as needed.

    Examples:
    >>> from opperai import fn
    >>> from pydantic import BaseModel

    >>> class Data(BaseModel):
    >>>     keywords: str
    >>>     sentiment: str

    >>> @fn
    >>> def extract(text = str) -> Data:
    >>>     ''' Extract keywords and sentiment from text. '''

    >>> result = extract(text="Opper is a lovely API that wraps the world of AI")
    >>> print(results)
    """

    def decorator(func):
        func_path = path or func.__name__
        setup_done = False
        sync_client = None
        _client = None
        _f = None

        def _prepare_function():
            use_few_shot = few_shot or os.environ.get("OPPER_USE_FEW_SHOT", False)
            function = FunctionIn(
                path=func_path,
                description=func.__doc__,
                instructions=f"Operation: {func.__name__}\n\nOperation description: {func.__doc__}",
                out_schema=get_output_schema(func),
                few_shot=use_few_shot,
            )
            if use_few_shot:
                function.use_semantic_search = True
                function.few_shot_count = few_shot_count or 2
            if cache_config:
                function.cache_configuration = cache_config

            function.model = (
                model if model else os.environ.get("OPPER_DEFAULT_MODEL", None)
            )

            return function

        def setup():
            nonlocal setup_done, sync_client, _client, _f
            if setup_done:
                return

            sync_client, async_client = _clients(client)
            _f = sync_client.functions.create(_prepare_function())

            if asyncio.iscoroutinefunction(func):
                _client = async_client
            else:
                _client = sync_client

            setup_done = True

        async def async_setup():
            nonlocal setup_done, sync_client, _client, _f
            if setup_done:
                return

            sync_client, async_client = _clients(client)
            _f = await async_client.functions.create(_prepare_function())

            _client = async_client

            setup_done = True

        def _unmarshal_response(response, return_type):
            if return_type is not None:
                if inspect.isclass(return_type) and issubclass(return_type, BaseModel):
                    response = return_type(**response)
                elif (
                    (get_origin(return_type) == list or get_origin(return_type) == List)
                    and inspect.isclass(get_args(return_type)[0])
                    and issubclass(get_args(return_type)[0], BaseModel)
                ):
                    response = [get_args(return_type)[0](**item) for item in response]
            return response

        def _prepare_payload(input, images):
            messages = [
                Message(role="user", content=json.dumps(input, cls=json_encoder))
            ]
            if images:
                messages.append(Message(role="user", content=images))

            return ChatPayload(
                parent_span_uuid=get_current_span_id(),
                messages=messages,
            )

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            answer, _ = await async_call(*args, **kwargs)
            return answer

        async def async_call(*args, **kwargs):
            await async_setup()

            input, media = convert_function_call_to_json(func, *args, **kwargs)
            _response = await _client.functions.chat(
                _f.uuid, _prepare_payload(input, media)
            )

            _thread_local.span_id = _response.span_id

            return_type = get_type_hints(func).get("return")
            answer = _unmarshal_response(_response.json_payload, return_type)

            response = AsyncFunctionResponse(client=_client, **_response.model_dump())

            return answer, response

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            answer, _ = sync_call(*args, **kwargs)
            return answer

        def sync_call(*args, **kwargs):
            setup()

            input, media = convert_function_call_to_json(func, *args, **kwargs)
            _response = _client.functions.chat(_f.uuid, _prepare_payload(input, media))

            _thread_local.span_id = _response.span_id

            return_type = get_type_hints(func).get("return")
            answer = _unmarshal_response(_response.json_payload, return_type)

            response = FunctionResponse(client=_client, **_response.model_dump())

            return answer, response

        if asyncio.iscoroutinefunction(func):
            async_wrapper.call = async_call
            return async_wrapper
        else:
            sync_wrapper.call = sync_call
            return sync_wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)
