from dataclasses import dataclass
from typing import List, Optional

from opperai._client import Client
from opperai.types.indexes import Document, Filter, RetrievalResponse
from opperai.types.indexes import Index as IndexModel


@dataclass
class Index:
    _client: Client
    _index: IndexModel

    def upload_file(self, file_path: str, **kwargs):
        """Upload a file to the index."""
        return self._client.indexes.upload_file(
            id=self._index.id, file_path=file_path, **kwargs
        )

    def add(self, doc: Document) -> Document:
        """Index a document."""
        return self._client.indexes.index(id=self._index.id, doc=doc)

    def query(
        self,
        query: str,
        k: int = 10,
        filters: List[Filter] = None,
        **kwargs,
    ) -> List[RetrievalResponse]:
        """Retrieve documents from the index."""

        return self._client.indexes.retrieve(
            id=self._index.id, query=query, k=k, filters=filters, **kwargs
        )

    def delete(self) -> bool:
        """Delete the index."""
        return self._client.indexes.delete(id=self._index.id)


class Indexes:
    _client: Client = None

    def __init__(self, client: Client = None):
        if client is None:
            client = Client()

        self._client = client

    def create(self, name: str) -> Index:
        """Create an index with the given name.

        If an index with the given name already exists, return it.
        """
        try:
            index = self.get(name=name)
            if index:
                return index
        except Exception:
            pass

        index = self._client.indexes.create(name=name)
        return Index(self._client, index)

    def get(self, id: int = None, name: str = None) -> Optional[Index]:
        """Get an index by id or name."""
        if id is not None:
            index = self._client.indexes.get(id=id)
        elif name is not None:
            index = self._client.indexes.get(name=name)
        else:
            raise ValueError("Either id or name must be provided")

        if not index:
            return None

        return Index(self._client, index)

    def delete(self, id: int) -> bool:
        """Delete an index by id."""
        return self._client.indexes.delete(id=id)

    def list(self) -> List[Index]:
        """List all indexes for the organization owning the API key."""
        indexes = self._client.indexes.list()
        return [Index(self._client, index) for index in indexes]
