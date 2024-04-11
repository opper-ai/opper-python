from typing import List, Optional

from opperai._http_clients import _async_http_client
from opperai.types.exceptions import APIError
from opperai.types.indexes import (
    Document,
    Filter,
    Index,
    RetrievalResponse,
)
from ._indexes import RetrieveQuery


class AsyncIndexes:
    def __init__(self, http_client: _async_http_client):
        self.http_client = http_client

    async def create(self, name: str) -> Index:
        response = await self.http_client.do_request(
            "POST",
            "/v1/indexes",
            json={"name": name},
        )
        if response.status_code != 200:
            raise APIError(f"Failed to create index with status {response.status_code}")
        return Index.model_validate(response.json())

    async def delete(self, id: int) -> bool:
        response = await self.http_client.do_request(
            "DELETE",
            f"/v1/indexes/{id}",
        )
        if response.status_code == 404:
            return False
        if response.status_code != 200:
            raise APIError(f"Failed to delete index with status {response.status_code}")
        return True

    async def get(self, id: int = None, name: str = None) -> Index:
        if id is None and name is None:
            raise ValueError("Either id or name must be provided")
        if id is not None and name is not None:
            raise ValueError("Only one of id or name should be provided")

        if id is not None:
            return await self._get_by_id(id)
        if name is not None:
            return await self._get_by_name(name)

    async def _get_by_id(self, id: int) -> Index:
        response = await self.http_client.do_request(
            "GET",
            f"/v1/indexes/{id}",
        )
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise APIError(
                f"Failed to get index {id} with status {response.status_code}"
            )
        return Index.model_validate(response.json())

    async def _get_by_name(self, name: str) -> Index:
        indexes = await self.list()
        for index in indexes:
            if index.name == name:
                return index
        return None

    async def list(self) -> List[Index]:
        response = await self.http_client.do_request(
            "GET",
            "/v1/indexes",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to list indexes with status {response.status_code}")
        return [Index.model_validate(item) for item in response.json()]

    async def upload_file(self, id: int, file_path: str, **kwargs):
        # Get upload URL
        upload_url_response = await self.http_client.do_request(
            "GET",
            f"/v1/indexes/{id}/upload_url",
            params={"filename": file_path.split("/")[-1]},
        )
        if upload_url_response.status_code != 200:
            raise APIError(
                f"Failed to get upload URL with status {upload_url_response.status_code}"
            )
        upload_url_data = upload_url_response.json()

        # Upload file
        with open(file_path, "rb") as file:
            files = {"file": (file_path.split("/")[-1], file)}
            upload_response = await self.http_client.do_request(
                "POST",
                upload_url_data["url"],
                files=files,
                data=upload_url_data["fields"],
            )
            if upload_response.status_code not in [200, 204]:
                raise APIError(
                    f"Failed to upload file with status {upload_response.status_code}"
                )

        # Register file
        register_file_response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/{id}/register_file",
            json={"uuid": upload_url_data["uuid"], **kwargs},
        )
        if register_file_response.status_code != 200:
            raise APIError(
                f"Failed to register file with status {register_file_response.status_code}"
            )

        return register_file_response.json()

    async def index(self, id: int, doc: Document) -> Document:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/{id}/index",
            json=doc.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to add document with status {response.status_code}")
        return Document.model_validate(response.json())

    async def retrieve(
        self, id: int, query: str, k: int, filters: Optional[List[Filter]] = None
    ) -> List[RetrievalResponse]:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/{id}/query",
            json=RetrieveQuery(q=query, k=k, filters=filters).model_dump(),
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to retrieve index {id} with status {response.status_code}"
            )
        return [RetrievalResponse.model_validate(item) for item in response.json()]
