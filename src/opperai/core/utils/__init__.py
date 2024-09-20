import json
from datetime import datetime
from inspect import signature
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel

from opperai.types import Example


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


def prepare_examples(examples: Optional[List[Example]]) -> List[Example]:
    _examples = []
    if examples:
        for example in examples:
            _input = prepare_input(example.input)
            _output = prepare_input(example.output)
            _examples.append(Example(input=str(_input), output=str(_output)))
    return _examples


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        # Let the base class default method raise the TypeError
        return super().default(obj)
