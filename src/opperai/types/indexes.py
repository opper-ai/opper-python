import datetime
from typing import Annotated, List, Optional, Union

from pydantic import UUID4, BaseModel, Field, field_validator


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


class Filter(BaseModel):
    key: str
    operation: Annotated[str, Field(pattern=r"^=|!=|>|<|in$")]
    value: Union[str, int, float, List[Union[str, int, float]]]
