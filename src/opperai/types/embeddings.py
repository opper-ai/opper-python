from typing import Any, List, Optional, Union

from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    """Request model for embeddings API."""

    model: str
    input: Union[str, List[str]]
    encoding_format: Optional[str] = None
    user: Optional[str] = None


class EmbeddingResponse(BaseModel):
    """Response model for embeddings API."""

    object: str = "list"
    model: str
    data: List[Any]
    usage: dict
