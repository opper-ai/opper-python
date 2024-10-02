from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from opperai._client import AsyncClient
from opperai.types.indexes import Document, DocumentIn, Filter, RetrievalResponse
from opperai.types.indexes import Index as IndexModel


@dataclass
class AsyncIndex:
    _client: AsyncClient
    _index: IndexModel

    async def upload_file(self, file_path: str, **kwargs):
        """Upload a file to the index."""
        return await self._client.indexes.upload_file(
            uuid=self._index.uuid, file_path=file_path, **kwargs
        )

    async def add(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        key: Optional[str] = None,
    ) -> Document:
        """Index a document."""
        return await self._client.indexes.index(
            uuid=self._index.uuid,
            doc=DocumentIn(content=content, metadata=metadata or {}, key=key),
        )

    async def query(
        self,
        query: str,
        k: int = 10,
        filters: List[Filter] = None,
        parent_span_uuid: Optional[str] = None,
        **kwargs,
    ) -> List[RetrievalResponse]:
        """Retrieve documents from the index."""

        return await self._client.indexes.retrieve(
            uuid=self._index.uuid,
            query=query,
            k=k,
            filters=filters,
            parent_span_uuid=parent_span_uuid,
            **kwargs,
        )

    async def delete(self) -> bool:
        """Delete the index."""
        return await self._client.indexes.delete(uuid=self._index.uuid)


class AsyncIndexes:
    _client: AsyncClient = None

    def __init__(self, client: AsyncClient = None):
        if client is None:
            client = AsyncClient()

        self._client = client

    async def create(
        self, name: str, embedding_model: str = "text-embedding-ada-002"
    ) -> AsyncIndex:
        """Create an index with the given name.

        If an index with the given name already exists, return it.
        """
        try:
            index = await self.get(name=name)
            if index:
                return index
        except Exception:
            pass

        index = await self._client.indexes.create(
            name=name, embedding_model=embedding_model
        )
        return AsyncIndex(self._client, index)

    async def get(self, uuid: str = None, name: str = None) -> Optional[AsyncIndex]:
        """Get an index by uuid or name."""
        if uuid is not None:
            index = await self._client.indexes.get(uuid=uuid)
        elif name is not None:
            index = await self._client.indexes.get(name=name)
        else:
            raise ValueError("Either uuid or name must be provided")

        if not index:
            return None

        return AsyncIndex(self._client, index)

    async def delete(self, uuid: str) -> bool:
        """Delete an index by uuid."""
        return await self._client.indexes.delete(uuid=uuid)

    async def list(self) -> List[AsyncIndex]:
        """List all indexes for the organization owning the API key."""
        indexes = await self._client.indexes.list()
        return [AsyncIndex(self._client, index) for index in indexes]
