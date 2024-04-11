import asyncio
import datetime
import json
import os
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Optional
from uuid import uuid4

from opperai import Client
from opperai.spans import _current_span_id
from opperai.types.spans import Span
from opperai.utils import convert_function_call_to_json


class SpanContext:
    def __init__(self, client: Client, span_uuid: str):
        self.client = client
        self.span_uuid = span_uuid
        self.output = None


@contextmanager
def start_span(
    name: str,
    input: Optional[str] = None,
    metadata: Optional[dict] = None,
    client: Optional[Client] = None,
):
    c = client if client is not None else Client()
    project = os.environ.get("OPPER_PROJECT", "missing_project")
    parent_span_id = _current_span_id.get()
    span_id = str(uuid4())
    span = Span(
        uuid=span_id,
        meta=metadata,
        input=input,
        parent_uuid=parent_span_id if parent_span_id is not None else None,
        project=project,
        name=name,
        start_time=datetime.datetime.utcnow(),
    )
    span_uuid = c.spans.create(span)

    span_token = _current_span_id.set(span_id)
    span_context = SpanContext(c, span_uuid)
    try:
        yield span_context  # This allows the block inside the 'with' statement to execute and interact with the span_context
    finally:
        end_time = datetime.datetime.utcnow()
        update_kwargs = {
            "end_time": end_time,
        }
        if span_context.output is not None:
            update_kwargs["output"] = span_context.output

        c.spans.update(span_uuid, **update_kwargs)
        _current_span_id.reset(span_token)


def trace(
    _func: Optional[Callable] = None,
    *,
    name: Optional[str] = None,
    client: Optional[Client] = None,
    trace_io: bool = False,
):
    def decorator_trace(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            c = client if client is not None else Client()

            project = os.environ.get("OPPER_PROJECT", "missing_project")
            parent_span_id = _current_span_id.get()
            span_id = str(uuid4())
            span_name = name if name is not None else func.__name__
            inputs = None
            if trace_io:
                inputs = json.dumps(
                    convert_function_call_to_json(func, *args, **kwargs)
                )
            span = Span(
                uuid=span_id,
                parent_uuid=parent_span_id if parent_span_id is not None else None,
                project=project,
                name=span_name,
                input=inputs,
                start_time=datetime.datetime.utcnow(),
            )
            span_uuid = c.spans.create(span)

            span_token = _current_span_id.set(span_id)
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                c.spans.update(
                    span_uuid,
                    end_time=datetime.datetime.utcnow(),
                    output=json.dumps(result) if trace_io else None,
                )
            finally:
                _current_span_id.reset(span_token)

            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            c = client if client is not None else Client()
            project = os.environ.get("OPPER_PROJECT", "missing_project")
            parent_span_id = _current_span_id.get()
            span_id = str(uuid4())
            span_name = name if name is not None else func.__name__
            inputs = None
            if trace_io:
                inputs = json.dumps(
                    convert_function_call_to_json(func, *args, **kwargs)
                )
            span = Span(
                uuid=span_id,
                parent_uuid=parent_span_id if parent_span_id is not None else None,
                project=project,
                name=span_name,
                input=inputs,
                start_time=datetime.datetime.utcnow(),
            )
            span_uuid = c.spans.create(span)

            span_token = _current_span_id.set(span_id)
            try:
                result = func(*args, **kwargs)
                c.spans.update(
                    span_uuid,
                    end_time=datetime.datetime.utcnow(),
                    output=json.dumps(result) if trace_io else None,
                )
            finally:
                _current_span_id.reset(span_token)

            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    if _func is None:
        return decorator_trace
    else:
        return decorator_trace(_func)
