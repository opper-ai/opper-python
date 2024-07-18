from typing import List

from opperai.core._http_clients import _async_http_client
from opperai.types.datasets import (
    DatasetEntry,
    DatasetEntryResponse,
    DatasetEntryUpdate,
)
from opperai.types.exceptions import APIError


class AsyncDatasets:
    def __init__(self, http_client: _async_http_client):
        self.http_client = http_client

    async def add(self, dataset_uuid: str, entry: DatasetEntry) -> str:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/datasets/{dataset_uuid}",
            json=entry.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to add entry with status {response.status_code}")
        return response.json()

    async def get_entries(
        self, dataset_uuid: str, offset: int = 0, limit: int = 100
    ) -> List[DatasetEntryResponse]:
        response = await self.http_client.do_request(
            "GET",
            f"/v1/datasets/{dataset_uuid}/entries",
            params={"offset": offset, "limit": limit},
        )
        if response.status_code != 200:
            raise APIError(f"Failed to get entries with status {response.status_code}")
        return [DatasetEntryResponse.model_validate(item) for item in response.json()]

    async def get_entry(
        self, dataset_uuid: str, entry_uuid: str
    ) -> DatasetEntryResponse:
        response = await self.http_client.do_request(
            "GET",
            f"/v1/datasets/{dataset_uuid}/entries/{entry_uuid}",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to get entry with status {response.status_code}")
        return DatasetEntryResponse.model_validate(response.json())

    async def update_entry(
        self, dataset_uuid: str, entry_uuid: str, entry: DatasetEntryUpdate
    ) -> DatasetEntryResponse:
        response = await self.http_client.do_request(
            "PUT",
            f"/v1/datasets/{dataset_uuid}/entries/{entry_uuid}",
            json=entry.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to update entry with status {response.status_code}")
        return DatasetEntryResponse.model_validate(response.json())

    async def delete_entry(self, dataset_uuid: str, entry_uuid: str) -> bool:
        response = await self.http_client.do_request(
            "DELETE",
            f"/v1/datasets/{dataset_uuid}/entries/{entry_uuid}",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to delete entry with status {response.status_code}")
        return response.json()
