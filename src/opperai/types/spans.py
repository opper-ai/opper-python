from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class GenerationIn(BaseModel):
    called_at: datetime
    duration_ms: int
    model: Optional[str] = None
    input: Optional[str] = None
    response: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    error: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = None
    cost: Optional[float] = None


class GenerationOut(GenerationIn):
    uuid: UUID


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
    generation: Optional[GenerationIn] = None


class SpanMetric(BaseModel):
    dimension: Optional[str] = None
    value: Optional[float] = None
    comment: Optional[str] = None
