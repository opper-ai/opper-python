import json
from datetime import datetime
from inspect import signature
from uuid import UUID

from opperai.types import ImageMessageContent
from pydantic import BaseModel


def convert_function_call_to_json(func, *args, **kwargs):
    media = []
    input_data = dict(zip(signature(func).parameters, args))
    input_data.update(kwargs)

    input = {}
    for key, value in input_data.items():
        if isinstance(value, ImageMessageContent):
            media.append(value)
        elif isinstance(value, BaseModel):
            input[key] = value.model_dump()
        elif isinstance(value, list) and all(isinstance(v, BaseModel) for v in value):
            input[key] = [v.model_dump() for v in value]
        else:
            input[key] = value

    return input, media


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        # Let the base class default method raise the TypeError
        return super().default(obj)
