import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class IndexRetrieveResponse(BaseModel):
    content: str
    metadata: dict


class DocumentIn(BaseModel):
    id: Optional[str] = None
    key: Optional[str] = None
    content: str = Field(..., min_length=1)
    metadata: dict = dict()


class DocumentOut(BaseModel):
    id: int
    uuid: UUID4
    key: str


class IndexOut(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
