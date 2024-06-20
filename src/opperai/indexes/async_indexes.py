from dataclasses import dataclass
from typing import List, Optional

from opperai._client import AsyncClient
from opperai.types.indexes import Document, Filter, RetrievalResponse
from opperai.types.indexes import Index as IndexModel


@dataclass
class AsyncIndex:
    _client: AsyncClient
    _index: IndexModel

    async def upload_file(self, file_path: str, **kwargs):
        """Upload a file to the index."""
        return await self._client.indexes.upload_file(
            id=self._index.id, file_path=file_path, **kwargs
        )

    async def add(self, doc: Document) -> Document:
        """Index a document."""
        return await self._client.indexes.index(id=self._index.id, doc=doc)

    async def query(
        self,
        query: str,
        k: int = 10,
        filters: List[Filter] = None,
        **kwargs,
    ) -> List[RetrievalResponse]:
        """Retrieve documents from the index."""

        return await self._client.indexes.retrieve(
            id=self._index.id, query=query, k=k, filters=filters, **kwargs
        )

    async def delete(self) -> bool:
        """Delete the index."""
        return await self._client.indexes.delete(id=self._index.id)


class AsyncIndexes:
    _client: AsyncClient = None

    def __init__(self, client: AsyncClient = None):
        if client is None:
            client = AsyncClient()

        self._client = client

    async def create(self, name: str) -> AsyncIndex:
        """Create an index with the given name.

        If an index with the given name already exists, return it.
        """
        try:
            index = await self.get(name=name)
            if index:
                return index
        except Exception:
            pass

        index = await self._client.indexes.create(name=name)
        return AsyncIndex(self._client, index)

    async def get(self, id: int = None, name: str = None) -> Optional[AsyncIndex]:
        """Get an index by id or name."""
        if id is not None:
            index = await self._client.indexes.get(id=id)
        elif name is not None:
            index = await self._client.indexes.get(name=name)
        else:
            raise ValueError("Either id or name must be provided")

        if not index:
            return None

        return AsyncIndex(self._client, index)

    async def delete(self, id: int) -> bool:
        """Delete an index by id."""
        return await self._client.indexes.delete(id=id)

    async def list(self) -> List[AsyncIndex]:
        """List all indexes for the organization owning the API key."""
        indexes = await self._client.indexes.list()
        return [AsyncIndex(self._client, index) for index in indexes]
