import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class DatasetEntry(BaseModel):
    input: str
    output: str
    expected: Optional[str] = None
    comment: Optional[str] = None


class DatasetEntryResponse(BaseModel):
    uuid: str
    input: str
    output: str
    expected: Optional[str] = None
    comment: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    span_id: Optional[UUID4] = None
    trace_id: Optional[UUID4] = None


class DatasetEntryUpdate(BaseModel):
    input: Optional[str] = None
    output: Optional[str] = None
    expected: Optional[str] = None
    comment: Optional[str] = None
