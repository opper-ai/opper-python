import asyncio
import contextlib
import inspect
import os
import threading
from functools import wraps
from typing import List, Optional, Union, get_args, get_origin, get_type_hints

from opperai._client import AsyncClient, Client
from opperai._opper import AsyncOpper, Opper
from opperai.core.utils import convert_function_call_to_json
from opperai.functions.async_functions import AsyncFunctionResponse
from opperai.functions.functions import Function, FunctionResponse
from opperai.types import (
    CacheConfiguration,
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


def get_last_span_id() -> Optional[str]:
    """Retrieve the last span ID from thread-local storage."""
    span_id = getattr(_thread_local, "span_id", None)
    if span_id is None:
        return None
    return str(span_id)


def fn(
    _func=None,
    *,
    path=None,
    client: Union[Client, AsyncClient, None] = None,
    json_encoder=None,
    model=None,
    few_shot=None,
    few_shot_count=None,
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
        client: Union[Client, AsyncClient, None] = None
        opper: Union[Opper, AsyncOpper, None] = None
        function: Function = None

        def _create_function(opper: Opper):
            return opper.functions.create(
                name=func_path,
                instructions=f"Operation: {func.__name__}\n\nOperation description: {func.__doc__}",
                description=func.__doc__,
                output_type=get_output_schema(func),
                model=model if model else os.environ.get("OPPER_DEFAULT_MODEL", None),
            )

        async def _create_function_async(opper: AsyncOpper):
            return await opper.functions.create(
                name=func_path,
                instructions=f"Operation: {func.__name__}\n\nOperation description: {func.__doc__}",
                description=func.__doc__,
                output_type=get_output_schema(func),
                model=model if model else os.environ.get("OPPER_DEFAULT_MODEL", None),
            )

        def setup():
            nonlocal setup_done, client, function, opper
            if setup_done:
                return

            if isinstance(client, AsyncClient):
                client = Client(api_key=client.api_key, api_url=client.api_url)
                opper = Opper(client)
            elif isinstance(client, Client):
                opper = Opper(client)
            else:
                client = Client()
                opper = Opper(client)

            function = _create_function(opper)

            if asyncio.iscoroutinefunction(func):
                client = AsyncClient(api_key=client.api_key, api_url=client.api_url)
                opper = AsyncOpper(client)
            else:
                client = client

            setup_done = True

        async def async_setup():
            nonlocal setup_done, client, function, opper
            if setup_done:
                return

            if isinstance(client, AsyncClient):
                opper = AsyncOpper(client)
            elif isinstance(client, Client):
                client = AsyncClient(api_key=client.api_key, api_url=client.api_url)
                opper = AsyncOpper(client)
            else:
                client = AsyncClient()
                opper = AsyncOpper(client)

            function = await _create_function_async(opper)

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

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            answer, _ = await async_call(*args, **kwargs)
            return answer

        async def async_call(*args, **kwargs):
            await async_setup()

            input = convert_function_call_to_json(func, *args, **kwargs)
            _result, _response = await function.call(
                input=input,
            )

            _thread_local.span_id = _response.span_id

            return_type = get_type_hints(func).get("return")
            answer = _unmarshal_response(_result, return_type)

            response = AsyncFunctionResponse(client=client, **_response.model_dump())

            return answer, response

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            answer, _ = sync_call(*args, **kwargs)
            return answer

        def sync_call(*args, **kwargs):
            setup()
            nonlocal function

            input = convert_function_call_to_json(func, *args, **kwargs)
            _result, _response = function.call(
                input=input,
            )

            _thread_local.span_id = _response.span_id

            return_type = get_type_hints(func).get("return")
            answer = _unmarshal_response(_result, return_type)

            response = FunctionResponse(client=client, **_response.model_dump())

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
