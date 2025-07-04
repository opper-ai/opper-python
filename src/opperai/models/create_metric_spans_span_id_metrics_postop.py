"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .createspanmetricrequest import (
    CreateSpanMetricRequest,
    CreateSpanMetricRequestTypedDict,
)
from opperai.types import BaseModel
from opperai.utils import FieldMetadata, PathParamMetadata, RequestMetadata
from typing_extensions import Annotated, TypedDict


class CreateMetricSpansSpanIDMetricsPostRequestTypedDict(TypedDict):
    span_id: str
    r"""The id of the span"""
    create_span_metric_request: CreateSpanMetricRequestTypedDict


class CreateMetricSpansSpanIDMetricsPostRequest(BaseModel):
    span_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The id of the span"""

    create_span_metric_request: Annotated[
        CreateSpanMetricRequest,
        FieldMetadata(request=RequestMetadata(media_type="application/json")),
    ]
