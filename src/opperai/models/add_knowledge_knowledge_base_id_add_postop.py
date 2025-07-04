"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .addrequest import AddRequest, AddRequestTypedDict
from opperai.types import BaseModel
from opperai.utils import FieldMetadata, PathParamMetadata, RequestMetadata
from typing_extensions import Annotated, TypedDict


class AddKnowledgeKnowledgeBaseIDAddPostRequestTypedDict(TypedDict):
    knowledge_base_id: str
    r"""The id of the knowledge base to add the data to"""
    add_request: AddRequestTypedDict


class AddKnowledgeKnowledgeBaseIDAddPostRequest(BaseModel):
    knowledge_base_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The id of the knowledge base to add the data to"""

    add_request: Annotated[
        AddRequest,
        FieldMetadata(request=RequestMetadata(media_type="application/json")),
    ]
