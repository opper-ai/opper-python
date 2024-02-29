import asyncio
import contextvars
import datetime
import json
import os
from functools import wraps
from typing import Callable, Optional
from uuid import uuid4

from opperai import Client
from opperai.types.events import Event
from opperai.utils import convert_function_call_to_json

_current_event_id = contextvars.ContextVar("_current_event_id", default=None)


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
            parent_event_id = _current_event_id.get()
            span_id = str(uuid4())
            event_name = name if name is not None else func.__name__
            inputs = None
            if trace_io:
                inputs = json.dumps(
                    convert_function_call_to_json(func, *args, **kwargs)
                )
            event = Event(
                uuid=span_id,
                parent_uuid=parent_event_id if parent_event_id is not None else None,
                project=project,
                name=event_name,
                input=inputs,
                start_time=datetime.datetime.utcnow(),
            )
            event_uuid = c.events.create(event)

            event_token = _current_event_id.set(span_id)
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                c.events.update(
                    event_uuid,
                    end_time=datetime.datetime.utcnow(),
                    output=json.dumps(result) if trace_io else None,
                )
            finally:
                _current_event_id.reset(event_token)

            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            c = client if client is not None else Client()
            project = os.environ.get("OPPER_PROJECT", "missing_project")
            parent_event_id = _current_event_id.get()
            span_id = str(uuid4())
            event_name = name if name is not None else func.__name__
            inputs = None
            if trace_io:
                inputs = json.dumps(
                    convert_function_call_to_json(func, *args, **kwargs)
                )
            event = Event(
                uuid=span_id,
                parent_uuid=parent_event_id if parent_event_id is not None else None,
                project=project,
                name=event_name,
                input=inputs,
                start_time=datetime.datetime.utcnow(),
            )
            event_uuid = c.events.create(event)

            event_token = _current_event_id.set(span_id)
            try:
                result = func(*args, **kwargs)
                c.events.update(
                    event_uuid,
                    end_time=datetime.datetime.utcnow(),
                    output=json.dumps(result) if trace_io else None,
                )
            finally:
                _current_event_id.reset(event_token)

            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    if _func is None:
        return decorator_trace
    else:
        return decorator_trace(_func)
