# ruff: noqa: F401
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from .events import EventFeedback

from pydantic import BaseModel, ConfigDict, Field

from .validators import validate_id_xor_path


class Message(BaseModel):
    role: str
    content: str


class ChatPayload(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")
    parent_event_uuid: Optional[str] = None

    messages: List[Message]


class FileMetadata(BaseModel):
    file_name: str


class ContextData(BaseModel):
    index_id: int
    content: str
    metadata: Union[Optional[dict], FileMetadata] = Field(default=None)


class StreamingChunk(BaseModel):
    event_id: Optional[str] = None
    delta: Optional[str] = None
    error: Optional[str] = None
    context: Optional[List[ContextData]] = None


class FunctionResponse(BaseModel):
    event_id: Optional[str] = None
    message: Optional[str] = None
    json_payload: Optional[Union[dict, List, Any]] = None
    error: Optional[str] = None
    context: Optional[List[ContextData]] = None


class FunctionDescription(BaseModel):
    id: Optional[int] = None
    path: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_]+(\/[a-zA-Z0-9_-]+)*$",
        description="Path should not contain characters that could break URLs.",
    )
    description: str
    input_schema: Optional[Dict[str, Any]] = None
    out_schema: Optional[Dict[str, Any]] = None
    instructions: str
    model: Optional[str] = None
    index_ids: Optional[List[int]] = None
    use_semantic_search: Optional[bool] = None
    few_shot: Optional[bool] = None
    few_shot_count: Optional[int] = None
