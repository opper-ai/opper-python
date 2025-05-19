# ruff: noqa: F401
from __future__ import annotations

import base64
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, FilePath, computed_field

from .datasets import DatasetEntry
from .embeddings import EmbeddingRequest, EmbeddingResponse
from .indexes import Document, DocumentIn, Filter, RetrievalResponse
from .spans import SpanMetric
from .validators import validate_uuid_xor_path


class Metric(BaseModel):
    """Metric for evaluations"""

    dimension: Optional[str] = None
    value: float = 1.0
    comment: Optional[str] = None


@dataclass
class ImageOutput:
    """NOTE: Magic type used to indicate that the output is an image"""

    bytes: bytes


@dataclass
class BetaAudioOutput:
    """NOTE: Magic type used to indicate that the output is an audio file"""

    bytes: bytes
    transcript: Optional[str] = None


class AudioInput(BaseModel):
    """NOTE: AudioInput is a magic type used to indicate that the input is an audio file

    There is a known limitation that when used as part of structured input one
    cannot pass in a list of images, nor can it be used in a nested fashion.

    This is due to limitations when it comes to deduce the relationship between
    the input fields and the images
    """

    path: FilePath = Field(exclude=True, default=None)

    @computed_field
    @property
    def _opper_audio_input(self) -> str:
        data = None
        if self.path:
            suffix = self.path.suffix
            if suffix == ".mp3":
                with open(self.path, "rb") as mp3_file:
                    base64_mp3 = base64.b64encode(mp3_file.read()).decode("utf-8")
                data = f"data:audio/mp3;base64,{base64_mp3}"

        if not data:
            raise ValueError("File type not supported. Supported types: .mp3")

        return data

    @classmethod
    def from_path(cls, path: FilePath):
        return AudioInput(path=path)


class BetaAudioInput(BaseModel):
    """NOTE: AudioInput is a magic type used to indicate that the input is an audio file

    There is a known limitation that when used as part of structured input one
    cannot pass in a list of images, nor can it be used in a nested fashion.

    This is due to limitations when it comes to deduce the relationship between
    the input fields and the images
    """

    path: FilePath = Field(exclude=True, default=None)

    @computed_field
    @property
    def _opper_beta_audio_input(self) -> Dict[str, Any]:
        data = None
        if self.path:
            suffix = self.path.suffix
            if suffix == ".wav":
                with open(self.path, "rb") as wav_file:
                    base64_wav = base64.b64encode(wav_file.read()).decode("utf-8")
                return {
                    "type": "input_audio",
                    "input_audio": {
                        "data": base64_wav,
                        "format": "wav",
                    },
                }
            elif suffix == ".mp3":
                with open(self.path, "rb") as mp3_file:
                    base64_mp3 = base64.b64encode(mp3_file.read()).decode("utf-8")
                return {
                    "type": "input_audio",
                    "input_audio": {
                        "data": base64_mp3,
                        "format": "mp3",
                    },
                }

        if not data:
            raise ValueError("File type not supported. Supported types: .wav")

        return data

    @classmethod
    def from_path(cls, path: FilePath):
        return BetaAudioInput(path=path)


class FileInput(BaseModel):
    """NOTE: FileInput is a magic type used to indicate that the input is a file

    There is a known limitation that when used as part of structured input one
    cannot pass in a list of files, nor can it be used in a nested fashion.

    This is due to limitations when it comes to deduce the relationship between
    the input fields and the files
    """

    path: Optional[FilePath] = Field(exclude=True, default=None)

    @computed_field
    @property
    def _opper_file_input(self) -> str:
        if self.path:
            suffix = self.path.suffix
            if suffix == ".pdf":
                with open(self.path, "rb") as pdf_file:
                    base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
                return f"data:application/pdf;base64,{base64_pdf}"
            else:
                raise ValueError("File type not supported. Supported types: .pdf")

        raise ValueError("no path or url provided")

    @classmethod
    def from_path(cls, path: FilePath):
        return FileInput(path=path)


class ImageInput(BaseModel):
    """NOTE: ImageInput is a magic type used to indicate that the input is an image

    There is a known limitation that when used as part of structured input one
    cannot pass in a list of images, nor can it be used in a nested fashion.

    This is due to limitations when it comes to deduce the relationship between
    the input fields and the images
    """

    path: Optional[FilePath] = Field(exclude=True, default=None)

    @computed_field
    @property
    def _opper_image_input(self) -> str:
        if not self.path:
            raise ValueError("no path provided")

        # Initialize MIME types database if not already done
        if not mimetypes.inited:
            mimetypes.init()

        # Read the image file
        with open(self.path, "rb") as image_file:
            image_data = image_file.read()

        # Get MIME type based on file extension
        mime_type, _ = mimetypes.guess_type(str(self.path))

        # Verify it's a supported image type
        if mime_type == "image/png":
            data_uri_mime = "image/png"
        elif mime_type in ("image/jpeg", "image/jpg"):
            data_uri_mime = "image/jpeg"
        else:
            # Fallback to checking file headers if mime_type is None or not an image
            if image_data.startswith(b"\x89PNG\r\n\x1a\n"):
                # PNG signature
                data_uri_mime = "image/png"
            elif image_data.startswith(b"\xff\xd8\xff"):
                # JPEG signature
                data_uri_mime = "image/jpeg"
            else:
                raise ValueError(
                    "File type not supported. Supported types: png, jpg, jpeg"
                )

        # Encode image data
        base64_image = base64.b64encode(image_data).decode("utf-8")
        return f"data:{data_uri_mime};base64,{base64_image}"

    @classmethod
    def from_path(cls, path: FilePath):
        return ImageInput(path=path)


MediaInput = Union[ImageInput, AudioInput, BetaAudioInput, FileInput]


class Message(BaseModel):
    role: str
    content: Union[str, List[Dict[str, Any]], List[MediaInput], MediaInput]


class CallConfiguration(BaseModel):
    model_config: ConfigDict = ConfigDict(protected_namespaces=(), extra="allow")

    class Invocation(BaseModel):
        class FewShot(BaseModel):
            count: int = 0

        few_shot: FewShot = Field(
            FewShot(),
        )

    invocation: Invocation = Field(
        Invocation(),
    )
    model_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)


class CallPayload(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = "you are a helpful assistant"
    input_schema: Optional[Dict[str, Any]] = None
    input: Optional[Any] = None
    output_schema: Optional[Dict[str, Any]] = None
    model: Optional[str] = None
    examples: Optional[List[Example]] = Field(default=None, max_length=10)
    stream: bool = False
    parent_span_uuid: Optional[str] = None
    fallback_models: Optional[List[str]] = None
    configuration: Optional[CallConfiguration] = None
    tags: Optional[Dict[str, str]] = None


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
    json_payload: Optional[Union[Dict[str, Any], List[Any], Any]] = None
    audio: Optional[Dict[str, Any]] = None
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
    dataset_uuid: Optional[str] = None


class FunctionConfiguration(BaseModel):
    class Cache(BaseModel):
        exact_match_cache_ttl: Optional[int] = None
        semantic_cache_threshold: Optional[float] = None
        semantic_cache_ttl: Optional[int] = None

    cache: Optional[Cache] = Field(default=Cache())


class Example(BaseModel):
    input: Any
    output: Any


class Error(BaseModel):
    type: str
    message: str
    detail: Any


class Errors(BaseModel):
    errors: List[Error]
