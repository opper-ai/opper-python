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
        return self._client.indexes.upload_file(
            id=self._index.id, file_path=file_path, **kwargs
        )

    def index(self, doc: Document) -> Document:
        return self._client.indexes.index(id=self._index.id, doc=doc)

    def query(
        self, query: str, k: int = 10, filters: List[Filter] = None
    ) -> List[RetrievalResponse]:
        return self._client.indexes.retrieve(
            id=self._index.id, query=query, k=k, filters=filters
        )

    def delete(self) -> bool:
        return self._client.indexes.delete(id=self._index.id)


@dataclass
class Indexes:
    _client: Client = Client()

    def create(self, name: str) -> Index:
        try:
            index = self.get(name=name)
            if index:
                return index
        except Exception:
            pass

        index = self._client.indexes.create(name=name)
        return Index(self._client, index)

    def get(self, id: int = None, name: str = None) -> Optional[Index]:
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
        return self._client.indexes.delete(id=id)

    def list(self) -> List[Index]:
        indexes = self._client.indexes.list()
        return [Index(self._client, index) for index in indexes]
