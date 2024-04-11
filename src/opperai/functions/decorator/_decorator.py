import asyncio
import contextlib
import inspect
import json
import os
import threading
from functools import wraps
from typing import List, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from opperai import AsyncClient, Client
from opperai.spans import _current_span_id
from opperai.types import CacheConfiguration, ChatPayload, Function, Message

from ...utils import convert_function_call_to_json
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


def fn(
    _func=None,
    *,
    path=None,
    client=None,
    json_encoder=None,
    model=None,
    few_shot=None,
    few_shot_count=None,
    cache_config: CacheConfiguration = None,
):
    def decorator(func):
        func_path = path or func.__name__
        setup_done = False
        sync_client = None
        c = None

        def setup():
            nonlocal setup_done, sync_client, c
            if setup_done:
                return

            if isinstance(client, AsyncClient):
                sync_client = Client(api_key=client.api_key, api_url=client.api_url)
            elif isinstance(client, Client):
                sync_client = client
            else:
                sync_client = Client()

            use_few_shot = few_shot or os.environ.get("OPPER_USE_FEW_SHOT", False)
            function = Function(
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

            sync_client.functions.create(function)

            if asyncio.iscoroutinefunction(func):
                c = AsyncClient() or client
            else:
                c = sync_client or client

            setup_done = True

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            setup()
            input = convert_function_call_to_json(func, *args, **kwargs)
            payload = ChatPayload(
                parent_span_uuid=_current_span_id.get(),
                messages=[
                    Message(role="user", content=json.dumps(input, cls=json_encoder))
                ],
            )

            response = await c.functions.chat(func_path, payload)
            answer = response.json_payload

            _thread_local.span_id = response.span_id
            return_type = get_type_hints(func).get("return")

            if return_type is not None:
                if inspect.isclass(return_type) and issubclass(return_type, BaseModel):
                    answer = return_type(**answer)
                elif (
                    (get_origin(return_type) == list or get_origin(return_type) == List)
                    and inspect.isclass(get_args(return_type)[0])
                    and issubclass(get_args(return_type)[0], BaseModel)
                ):
                    answer = [get_args(return_type)[0](**item) for item in answer]
            return answer

        def sync_wrapper(*args, **kwargs):
            setup()
            input = convert_function_call_to_json(func, *args, **kwargs)
            payload = ChatPayload(
                parent_span_uuid=_current_span_id.get(),
                messages=[
                    Message(role="user", content=json.dumps(input, cls=json_encoder))
                ],
            )
            response = c.functions.chat(func_path, payload)
            answer = response.json_payload
            _thread_local.span_id = response.span_id

            return_type = get_type_hints(func).get("return")
            if return_type is not None:
                if inspect.isclass(return_type) and issubclass(return_type, BaseModel):
                    answer = return_type(**answer)
                elif (
                    (get_origin(return_type) == list or get_origin(return_type) == List)
                    and inspect.isclass(get_args(return_type)[0])
                    and issubclass(get_args(return_type)[0], BaseModel)
                ):
                    answer = [get_args(return_type)[0](**item) for item in answer]
            return answer

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)
