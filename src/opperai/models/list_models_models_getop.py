"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from opperai.types import BaseModel
from opperai.utils import FieldMetadata, QueryParamMetadata
from typing import Optional
from typing_extensions import Annotated, NotRequired, TypedDict


class ListModelsModelsGetRequestTypedDict(TypedDict):
    offset: NotRequired[int]
    r"""The offset of the models to return when paginating"""
    limit: NotRequired[int]
    r"""The number of models to return per page when paginating"""


class ListModelsModelsGetRequest(BaseModel):
    offset: Annotated[
        Optional[int],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = 0
    r"""The offset of the models to return when paginating"""

    limit: Annotated[
        Optional[int],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = 100
    r"""The number of models to return per page when paginating"""
