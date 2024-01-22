from pydantic import BaseModel, Field
from typing import List, Optional


class Message(BaseModel):
    role: str
    content: str


class ChatPayload(BaseModel):
    messages: List[Message]


class ContextData(BaseModel):
    embeddings_id: str
    embeddings_table: str
    dataset_id: int
    content: str
    score: Optional[float]


class DebugData(BaseModel):
    context: List[ContextData]


class StreamingChunk(BaseModel):
    delta: str
    error: Optional[str] = None


class FunctionResponse(BaseModel):
    message: str
    error: Optional[str] = None
    debug: Optional[DebugData] = None
