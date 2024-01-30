import asyncio
import inspect
import json
from functools import wraps
from typing import List, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from opperai import AsyncClient, Client
from opperai.types import ChatPayload, FunctionDescription, Message

from ._schemas import convert_function_call_to_json, get_output_schema


def fn(path=None, client=None, json_encoder=None):
    def decorator(func):
        sync_client = Client()
        func_path = path or func.__name__

        function = FunctionDescription(
            path=func_path,
            description=func.__doc__,
            instructions=f"Operation: {func.__name__}\n\nOperation description: {func.__doc__}",
            out_schema=get_output_schema(func),
        )
        sync_client.functions.create_function(function)

        if asyncio.iscoroutinefunction(func):
            c = AsyncClient() or client
        else:
            c = sync_client or client

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            input = convert_function_call_to_json(func, *args, **kwargs)
            payload = ChatPayload(
                messages=[
                    Message(role="user", content=json.dumps(input, cls=json_encoder))
                ]
            )
            response = await c.functions.chat(func_path, payload)
            answer = response.json_payload

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
            input = convert_function_call_to_json(func, *args, **kwargs)
            payload = ChatPayload(
                messages=[
                    Message(role="user", content=json.dumps(input, cls=json_encoder))
                ]
            )
            answer = c.functions.chat(func_path, payload).json_payload

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

    return decorator
