"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from opperai.types import BaseModel
from opperai.utils import validate_const
import pydantic
from pydantic.functional_validators import AfterValidator
from typing import Literal
from typing_extensions import Annotated, TypedDict


class ResponseFormatTextTypedDict(TypedDict):
    type: Literal["text"]


class ResponseFormatText(BaseModel):
    TYPE: Annotated[
        Annotated[Literal["text"], AfterValidator(validate_const("text"))],
        pydantic.Field(alias="type"),
    ] = "text"
