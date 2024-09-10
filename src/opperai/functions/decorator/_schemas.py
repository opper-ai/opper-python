import inspect
from typing import Dict, List, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel


def type_to_json_schema(type_hint):
    if type_hint is None:
        return None

    # in case the type is a dict we assume it's a json schema
    if isinstance(type_hint, dict):
        return type_hint

    schema = _type_to_json_schema(type_hint)
    schema, defs = _lift_defs(schema, {})
    if defs:
        schema["$defs"] = defs

    return schema


def _lift_defs(schema: Dict, defs: Dict = {}):
    if "$defs" in schema:
        for k, v in schema["$defs"].items():
            defs[k] = v
        schema.pop("$defs")

    for k, v in schema.items():
        if isinstance(v, dict):
            _lift_defs(v, defs)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    _lift_defs(item, defs)

    return schema, defs


def _type_to_json_schema(type_hint):
    """Convert a Python type to a JSON schema."""
    if type_hint == int:
        return {"type": "integer"}
    elif type_hint == str:
        return {"type": "string"}
    elif type_hint == float:
        return {"type": "number"}
    elif type_hint == bool:
        return {"type": "boolean"}
    elif inspect.isclass(type_hint) and issubclass(type_hint, BaseModel):
        return type_hint.model_json_schema()
    elif hasattr(type_hint, "__origin__"):
        # Handling generic types (List, Dict, etc.)
        if get_origin(type_hint) == Union and type(None) in get_args(type_hint):
            return _type_to_json_schema(get_args(type_hint)[0])  # for Optional
        elif type_hint.__origin__ in (List, list):
            item_type = get_args(type_hint)[0]
            if inspect.isclass(item_type):
                return {"type": "array", "items": _type_to_json_schema(item_type)}
            if get_origin(item_type) == List:
                return {"type": "array", "items": _type_to_json_schema(item_type)}
            elif inspect.isclass(item_type) and issubclass(item_type, BaseModel):
                return {"type": "array", "items": item_type.model_json_schema()}
            else:
                return {"type": "array", "items": _type_to_json_schema(item_type)}
        elif get_origin(type_hint) == Dict:
            return {"type": "object"}
        else:
            raise NotImplementedError(
                f"Type {type_hint} is not supported for JSON schema generation.{get_origin(type_hint)}"
            )
    else:
        return {"type": "object"}


def get_input_schema(func):
    """Generate input JSON schema from a function signature."""
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    schema = {"type": "object", "properties": {}, "required": []}

    for param in sig.parameters.values():
        param_type = type_hints.get(
            param.name, str
        )  # Default to string if type is not specified
        schema["properties"][param.name] = type_to_json_schema(param_type)
        if param.default is inspect.Parameter.empty:
            schema["required"].append(param.name)

    if not schema["properties"]:
        return {
            "type": "object",
            "description": "No input parameters",
            "properties": {},
            "additionalProperties": False,
        }

    return schema


def get_output_schema(func):
    """Generate output JSON schema from a function signature."""
    return_type = get_type_hints(func).get("return", None)
    if return_type:
        schema = type_to_json_schema(return_type)
    else:
        schema = {"type": "unknown"}

    return schema
