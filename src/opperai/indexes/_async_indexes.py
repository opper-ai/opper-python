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

    async def get_by_name(self, name: str) -> IndexOut:
        indexes = await self.list()
        for index in indexes:
            if index.name == name:
                return index
        raise APIError(f"Index with name {name} not found")

    async def upload_file(self, index_id: int, file_path: str):
        # Get upload URL
        upload_url_response = await self.http_client.do_request(
            "GET",
            f"/v1/indexes/{index_id}/upload_url",
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
            f"/v1/indexes/{index_id}/register_file",
            json={"uuid": upload_url_data["uuid"]},
        )
        if register_file_response.status_code != 200:
            raise APIError(
                f"Failed to register file with status {register_file_response.status_code}"
            )

        return register_file_response.json()

    async def index(self, index_id: int, doc: DocumentIn) -> DocumentOut:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/{index_id}/index",
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
