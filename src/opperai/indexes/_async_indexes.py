from typing import List

from opperai._http_clients import _async_http_client
from opperai.types.exceptions import APIError
from opperai.types.indexes import (
    DocumentIn,
    DocumentOut,
    IndexOut,
    IndexRetrieveResponse,
)


class AsyncIndexes:
    def __init__(self, http_client: _async_http_client):
        self.http_client = http_client

    async def create(self, name: str) -> int:
        response = await self.http_client.do_request(
            "POST",
            "/v1/indexes",
            json={"name": name},
        )
        if response.status_code != 200:
            raise APIError(f"Failed to create index with status {response.status_code}")
        return response.json()["dataset_id"]

    async def delete(self, index_id: int):
        response = await self.http_client.do_request(
            "DELETE",
            f"/v1/indexes/{index_id}",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to delete index with status {response.status_code}")
        return response.json()

    async def list(self):
        response = await self.http_client.do_request(
            "GET",
            "/v1/indexes",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to list indexes with status {response.status_code}")
        return [IndexOut.model_validate(item) for item in response.json()]

    async def index(self, doc: DocumentIn) -> DocumentOut:
        response = await self.http_client.do_request(
            "POST",
            "/v1/indexes/index",
            json=doc.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to add document with status {response.status_code}")
        return DocumentOut.model_validate(response.json())

    async def retrieve(
        self, index_id: int, query: str, k: int
    ) -> List[IndexRetrieveResponse]:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/{index_id}/query",
            json={"q": query, "k": k},
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to retrieve index {index_id} with status {response.status_code}"
            )
        return [IndexRetrieveResponse.model_validate(item) for item in response.json()]
