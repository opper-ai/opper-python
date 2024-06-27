# ruff: noqa: F401

import base64
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, FilePath, computed_field

from .indexes import Document, DocumentIn, Filter, RetrievalResponse
from .spans import SpanMetric
from .validators import validate_uuid_xor_path


class TextMessageContent(BaseModel):
    type: str = "text"
    text: str


class ImageMessageUrl(BaseModel):
    url: str


class ImageMessageFile(BaseModel):
    path: FilePath = Field(exclude=True)

    @computed_field
    @property
    def url(self) -> str:
        path = self.path.as_posix()
        if path.endswith(".png"):
            with open(path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/png;base64,{base64_image}"
        elif path.endswith(".jpg"):
            with open(path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{base64_image}"
        elif path.endswith(".jpeg"):
            with open(path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{base64_image}"
        else:
            raise ValueError(
                "File type not supported. Supported types: .png, .jpg, .jpeg"
            )


class ImageMessageContent(BaseModel):
    type: str = "image_url"
    image_url: Union[ImageMessageUrl, ImageMessageFile]


class MessageContent(BaseModel):
    @classmethod
    def text(cls, text: str) -> TextMessageContent:
        return TextMessageContent(text=text)

    @classmethod
    def image(cls, path: str) -> ImageMessageContent:
        return ImageMessageContent(image_url=ImageMessageFile(path=path))

    @classmethod
    def image_url(cls, url: str) -> ImageMessageContent:
        return ImageMessageContent(image_url=ImageMessageUrl(url=url))


class ImageContent:
    @classmethod
    def from_path(cls, path: str) -> ImageMessageContent:
        return ImageMessageContent(image_url=ImageMessageFile(path=path))

    @classmethod
    def from_url(cls, url: str) -> ImageMessageContent:
        return ImageMessageContent(image_url=ImageMessageUrl(url=url))


class Message(BaseModel):
    role: str
    content: Union[str, List[Union[TextMessageContent, ImageMessageContent]]]


class ChatPayload(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")
    parent_span_uuid: Optional[str] = None

    messages: List[Message]


class FileMetadata(BaseModel):
    file_name: str


class ContextData(BaseModel):
    index_id: int
    content: str
    metadata: Union[Optional[dict], FileMetadata] = Field(default=None)


class StreamingChunk(BaseModel):
    span_id: Optional[str] = None
    delta: Optional[str] = None
    context: Optional[List[ContextData]] = None


class FunctionResponse(BaseModel):
    span_id: Optional[str] = None
    message: Optional[str] = None
    json_payload: Optional[Union[dict, List, Any]] = None
    context: Optional[List[ContextData]] = None
    cached: Optional[bool] = None


class CacheConfiguration(BaseModel):
    exact_match_cache_ttl: Optional[int] = None
    semantic_cache_threshold: Optional[float] = None
    semantic_cache_ttl: Optional[int] = None


class Function(BaseModel):
    uuid: Optional[str] = None
    path: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_]+(\/[a-zA-Z0-9_-]+)*$",
        description="Path should not contain characters that could break URLs.",
    )
    description: Optional[str] = None
    input_schema: Optional[Dict[str, Any]] = None
    out_schema: Optional[Dict[str, Any]] = None
    instructions: str
    model: Optional[str] = None
    index_ids: Optional[List[int]] = []
    use_semantic_search: Optional[bool] = None
    few_shot: Optional[bool] = None
    few_shot_count: Optional[int] = None
    cache_configuration: Optional[CacheConfiguration] = None


class Error(BaseModel):
    type: str
    message: str
    detail: Any


class Errors(BaseModel):
    errors: List[Error]
