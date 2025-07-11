"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from datetime import datetime
from opperai.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
from pydantic import model_serializer
from typing import Any, Dict
from typing_extensions import NotRequired, TypedDict


class GetSpanResponseTypedDict(TypedDict):
    name: str
    r"""The name of the span, something descriptive about the span that will be used to identify it when querying"""
    id: str
    start_time: NotRequired[Nullable[datetime]]
    r"""The start time of the span in UTC"""
    trace_id: NotRequired[Nullable[str]]
    r"""The id of the trace"""
    parent_id: NotRequired[Nullable[str]]
    r"""The id of the parent span"""
    type: NotRequired[Nullable[str]]
    r"""The type of the span"""
    end_time: NotRequired[Nullable[datetime]]
    r"""The end time of the span in UTC"""
    input: NotRequired[Nullable[Any]]
    r"""The input of the span"""
    output: NotRequired[Nullable[Any]]
    r"""The output of the span"""
    error: NotRequired[Nullable[str]]
    r"""In case of an error, the error message"""
    meta: NotRequired[Nullable[Dict[str, Any]]]
    r"""The metadata of the span"""
    score: NotRequired[Nullable[int]]
    r"""The score of the span"""


class GetSpanResponse(BaseModel):
    name: str
    r"""The name of the span, something descriptive about the span that will be used to identify it when querying"""

    id: str

    start_time: OptionalNullable[datetime] = UNSET
    r"""The start time of the span in UTC"""

    trace_id: OptionalNullable[str] = UNSET
    r"""The id of the trace"""

    parent_id: OptionalNullable[str] = UNSET
    r"""The id of the parent span"""

    type: OptionalNullable[str] = UNSET
    r"""The type of the span"""

    end_time: OptionalNullable[datetime] = UNSET
    r"""The end time of the span in UTC"""

    input: OptionalNullable[Any] = UNSET
    r"""The input of the span"""

    output: OptionalNullable[Any] = UNSET
    r"""The output of the span"""

    error: OptionalNullable[str] = UNSET
    r"""In case of an error, the error message"""

    meta: OptionalNullable[Dict[str, Any]] = UNSET
    r"""The metadata of the span"""

    score: OptionalNullable[int] = UNSET
    r"""The score of the span"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "start_time",
            "trace_id",
            "parent_id",
            "type",
            "end_time",
            "input",
            "output",
            "error",
            "meta",
            "score",
        ]
        nullable_fields = [
            "start_time",
            "trace_id",
            "parent_id",
            "type",
            "end_time",
            "input",
            "output",
            "error",
            "meta",
            "score",
        ]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in type(self).model_fields.items():
            k = f.alias or n
            val = serialized.get(k)
            serialized.pop(k, None)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m
