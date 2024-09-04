import json
from datetime import datetime
from inspect import signature
from typing import Any
from uuid import UUID

from pydantic import BaseModel


def convert_function_call_to_json(func, *args, **kwargs):
    input_data = dict(zip(signature(func).parameters, args))
    input_data.update(kwargs)

    return prepare_input(input_data)


def prepare_input(input: Any) -> Any:
    if isinstance(input, str):
        return input
    elif isinstance(input, BaseModel):
        return input.model_dump(exclude_none=True)
    elif isinstance(input, list):
        _input = [prepare_input(item) for item in input]
        return _input
    elif isinstance(input, dict):
        _input = {key: prepare_input(value) for key, value in input.items()}
        return _input
    else:
        return input


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        # Let the base class default method raise the TypeError
        return super().default(obj)
