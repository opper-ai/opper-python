"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from opperai import utils
from opperai.types import BaseModel
from typing import Any, Optional


class ConflictErrorData(BaseModel):
    detail: Any
    r"""The detail of the error"""

    type: Optional[str] = "ConflictError"

    message: Optional[str] = "The resource already exists"


class ConflictError(Exception):
    data: ConflictErrorData

    def __init__(self, data: ConflictErrorData):
        self.data = data

    def __str__(self) -> str:
        return utils.marshal_json(self.data, ConflictErrorData)
