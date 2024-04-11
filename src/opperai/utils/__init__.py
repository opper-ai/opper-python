import json
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


from inspect import signature


def convert_function_call_to_json(func, *args, **kwargs):
    input_data = dict(zip(signature(func).parameters, args))
    input_data.update(kwargs)
    for key, value in input_data.items():
        if isinstance(value, BaseModel):
            input_data[key] = value.model_dump()
        elif isinstance(value, list) and all(isinstance(v, BaseModel) for v in value):
            input_data[key] = [v.model_dump() for v in value]
    return input_data


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        # Let the base class default method raise the TypeError
        return super().default(obj)
