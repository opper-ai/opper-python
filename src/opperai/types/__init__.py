from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str


class ChatPayload(BaseModel):
    messages: List[Message]

    class Config:
        extra = "allow"


class FileMetadata(BaseModel):
    file_name: str


class ContextData(BaseModel):
    dataset_id: int
    content: str
    metadata: Union[Optional[dict], FileMetadata] = Field(default=None)


class StreamingChunk(BaseModel):
    delta: Optional[str] = None
    error: Optional[str] = None
    context: Optional[List[ContextData]] = None


class FunctionResponse(BaseModel):
    message: str = None
    json_payload: Optional[dict] = None
    error: Optional[str] = None
    context: Optional[List[ContextData]] = None
