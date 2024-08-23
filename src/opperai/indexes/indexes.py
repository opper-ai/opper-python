from dataclasses import dataclass
from typing import List, Optional

from opperai._client import Client
from opperai.types.indexes import Document, DocumentIn, Filter, RetrievalResponse
from opperai.types.indexes import Index as IndexModel


@dataclass
class Index:
    _client: Client
    _index: IndexModel

    def upload_file(self, file_path: str, **kwargs):
        """Upload a file to the index."""
        return self._client.indexes.upload_file(
            uuid=self._index.uuid, file_path=file_path, **kwargs
        )

    def add(self, doc: DocumentIn) -> Document:
        """Index a document."""
        return self._client.indexes.index(uuid=self._index.uuid, doc=doc)

    def query(
        self,
        query: str,
        k: int = 10,
        filters: List[Filter] = None,
        parent_span_uuid: Optional[str] = None,
        **kwargs,
    ) -> List[RetrievalResponse]:
        """Retrieve documents from the index."""

        return self._client.indexes.retrieve(
            uuid=self._index.uuid,
            query=query,
            k=k,
            filters=filters,
            parent_span_uuid=parent_span_uuid,
            **kwargs,
        )

    def delete(self) -> bool:
        """Delete the index."""
        return self._client.indexes.delete(uuid=self._index.uuid)


class Indexes:
    _client: Client = None

    def __init__(self, client: Client = None):
        if client is None:
            client = Client()

        self._client = client

    def create(
        self, name: str, embedding_model: str = "text-embedding-ada-002"
    ) -> Index:
        """Create an index with the given name.

        If an index with the given name already exists, return it.
        """
        try:
            index = self.get(name=name)
            if index:
                return index
        except Exception:
            pass

        index = self._client.indexes.create(name=name, embedding_model=embedding_model)
        return Index(self._client, index)

    def get(self, uuid: str = None, name: str = None) -> Optional[Index]:
        """Get an index by id or name."""
        if uuid is not None:
            index = self._client.indexes.get(uuid=uuid)
        elif name is not None:
            index = self._client.indexes.get(name=name)
        else:
            raise ValueError("Either uuid or name must be provided")

        if not index:
            return None

        return Index(self._client, index)

    def delete(self, uuid: str) -> bool:
        """Delete an index by id."""
        return self._client.indexes.delete(uuid=uuid)

    def list(self) -> List[Index]:
        """List all indexes for the organization owning the API key."""
        indexes = self._client.indexes.list()
        return [Index(self._client, index) for index in indexes]
