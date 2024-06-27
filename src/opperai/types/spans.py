from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Span(BaseModel):
    uuid: Optional[UUID] = None
    name: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    start_time: Optional[datetime] = None
    parent_uuid: Optional[UUID] = None
    end_time: Optional[datetime] = None
    error: Optional[str] = None
    meta: Optional[dict] = None
    evaluations: Optional[dict] = None
    score: Optional[int] = None


class SpanMetric(BaseModel):
    dimension: Optional[str] = None
    value: Optional[float] = None
    comment: Optional[str] = None
