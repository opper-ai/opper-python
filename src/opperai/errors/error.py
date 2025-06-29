"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from opperai import utils
from opperai.types import BaseModel
from typing import Any


class ErrorData(BaseModel):
    type: str

    message: str

    detail: Any


class Error(Exception):
    data: ErrorData

    def __init__(self, data: ErrorData):
        self.data = data

    def __str__(self) -> str:
        return utils.marshal_json(self.data, ErrorData)
