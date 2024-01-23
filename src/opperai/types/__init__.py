from pydantic import BaseModel, Field
from typing import List, Optional, Union


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
    message: str
    error: Optional[str] = None
    context: Optional[List[ContextData]] = None
