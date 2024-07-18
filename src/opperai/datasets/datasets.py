from dataclasses import dataclass
from typing import List

from opperai._client import Client
from opperai.types.datasets import (
    DatasetEntry,
    DatasetEntryResponse,
    DatasetEntryUpdate,
)


@dataclass
class Dataset:
    _client: Client
    _dataset_uuid: str

    def add(self, entry: DatasetEntry) -> str:
        """Add an entry to the dataset."""
        return self._client.datasets.add(dataset_uuid=self._dataset_uuid, entry=entry)

    def get_entries(
        self, offset: int = 0, limit: int = 100
    ) -> List[DatasetEntryResponse]:
        """Get entries from the dataset."""
        return self._client.datasets.get_entries(
            dataset_uuid=self._dataset_uuid, offset=offset, limit=limit
        )

    def get_entry(self, entry_uuid: str) -> DatasetEntryResponse:
        """Get a specific entry from the dataset."""
        return self._client.datasets.get_entry(
            dataset_uuid=self._dataset_uuid, entry_uuid=entry_uuid
        )

    def update_entry(
        self, entry_uuid: str, entry: DatasetEntryUpdate
    ) -> DatasetEntryResponse:
        """Update a specific entry in the dataset."""
        return self._client.datasets.update_entry(
            dataset_uuid=self._dataset_uuid, entry_uuid=entry_uuid, entry=entry
        )

    def delete_entry(self, entry_uuid: str) -> bool:
        """Delete a specific entry from the dataset."""
        return self._client.datasets.delete_entry(
            dataset_uuid=self._dataset_uuid, entry_uuid=entry_uuid
        )


class Datasets:
    _client: Client = None

    def __init__(self, client: Client = None):
        if client is None:
            client = Client()

        self._client = client

    def get(self, dataset_uuid: str) -> Dataset:
        """Get a dataset by its UUID."""
        return Dataset(self._client, dataset_uuid)

    def add(self, dataset_uuid: str, entry: DatasetEntry) -> str:
        """Add an entry to a dataset."""
        return self._client.datasets.add(dataset_uuid=dataset_uuid, entry=entry)

    def get_entries(
        self, dataset_uuid: str, offset: int = 0, limit: int = 100
    ) -> List[DatasetEntryResponse]:
        """Get entries from a dataset."""
        return self._client.datasets.get_entries(
            dataset_uuid=dataset_uuid, offset=offset, limit=limit
        )

    def get_entry(self, dataset_uuid: str, entry_uuid: str) -> DatasetEntryResponse:
        """Get a specific entry from a dataset."""
        return self._client.datasets.get_entry(
            dataset_uuid=dataset_uuid, entry_uuid=entry_uuid
        )

    def update_entry(
        self, dataset_uuid: str, entry_uuid: str, entry: DatasetEntryUpdate
    ) -> DatasetEntryResponse:
        """Update a specific entry in a dataset."""
        return self._client.datasets.update_entry(
            dataset_uuid=dataset_uuid, entry_uuid=entry_uuid, entry=entry
        )

    def delete_entry(self, dataset_uuid: str, entry_uuid: str) -> bool:
        """Delete a specific entry from a dataset."""
        return self._client.datasets.delete_entry(
            dataset_uuid=dataset_uuid, entry_uuid=entry_uuid
        )
