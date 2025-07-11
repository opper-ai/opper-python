"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .spandata import SpanData, SpanDataTypedDict
from .spanmetricdata import SpanMetricData, SpanMetricDataTypedDict
from datetime import datetime
from opperai.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
from pydantic import model_serializer
from typing import Any, Dict, List
from typing_extensions import NotRequired, TypedDict


class SpanSchemaTypedDict(TypedDict):
    id: NotRequired[Nullable[str]]
    r"""The id of the span, set to the uuid of the span"""
    name: NotRequired[Nullable[str]]
    r"""The name of the span"""
    start_time: NotRequired[Nullable[datetime]]
    r"""The start time of the span"""
    type: NotRequired[Nullable[str]]
    r"""The type of the span"""
    parent_id: NotRequired[Nullable[str]]
    r"""The id of the parent span"""
    end_time: NotRequired[Nullable[datetime]]
    r"""The end time of the span"""
    duration_ms: NotRequired[Nullable[int]]
    r"""The duration of the span in milliseconds"""
    error: NotRequired[Nullable[str]]
    r"""Optional error of the span"""
    meta: NotRequired[Nullable[Dict[str, Any]]]
    r"""The metadata of the span, can be used to add additional information about the span"""
    data: NotRequired[Nullable[SpanDataTypedDict]]
    r"""The data of the span"""
    metrics: NotRequired[Nullable[List[SpanMetricDataTypedDict]]]
    r"""The metrics of the span"""
    score: NotRequired[Nullable[int]]
    r"""The score of the span"""


class SpanSchema(BaseModel):
    id: OptionalNullable[str] = UNSET
    r"""The id of the span, set to the uuid of the span"""

    name: OptionalNullable[str] = UNSET
    r"""The name of the span"""

    start_time: OptionalNullable[datetime] = UNSET
    r"""The start time of the span"""

    type: OptionalNullable[str] = UNSET
    r"""The type of the span"""

    parent_id: OptionalNullable[str] = UNSET
    r"""The id of the parent span"""

    end_time: OptionalNullable[datetime] = UNSET
    r"""The end time of the span"""

    duration_ms: OptionalNullable[int] = UNSET
    r"""The duration of the span in milliseconds"""

    error: OptionalNullable[str] = UNSET
    r"""Optional error of the span"""

    meta: OptionalNullable[Dict[str, Any]] = UNSET
    r"""The metadata of the span, can be used to add additional information about the span"""

    data: OptionalNullable[SpanData] = UNSET
    r"""The data of the span"""

    metrics: OptionalNullable[List[SpanMetricData]] = UNSET
    r"""The metrics of the span"""

    score: OptionalNullable[int] = UNSET
    r"""The score of the span"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "id",
            "name",
            "start_time",
            "type",
            "parent_id",
            "end_time",
            "duration_ms",
            "error",
            "meta",
            "data",
            "metrics",
            "score",
        ]
        nullable_fields = [
            "id",
            "name",
            "start_time",
            "type",
            "parent_id",
            "end_time",
            "duration_ms",
            "error",
            "meta",
            "data",
            "metrics",
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
