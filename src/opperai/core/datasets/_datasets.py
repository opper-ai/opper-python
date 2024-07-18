from typing import List

from opperai.core._http_clients import _http_client
from opperai.types.datasets import (
    DatasetEntry,
    DatasetEntryResponse,
    DatasetEntryUpdate,
)
from opperai.types.exceptions import APIError


class Datasets:
    def __init__(self, http_client: _http_client):
        self.http_client = http_client

    def add(self, dataset_uuid: str, entry: DatasetEntry) -> str:
        """Add an entry to a dataset

        This method adds an entry to a specified dataset by its unique identifier. The entry is added to the dataset, making it part of the dataset's collection.

        Args:
            dataset_uuid (str): The unique identifier of the dataset.
            entry (DatasetEntrySchema): The entry to be added to the dataset.

        Returns:
            str: The unique identifier of the added entry.

        Raises:
            APIError: If the entry addition fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types.datasets import DatasetEntrySchema
            >>> client = Client(api_key="your_api_key_here")
            >>> entry = DatasetEntrySchema(input="Example input", output="Example output")
            >>> entry_uuid = client.datasets.add(dataset_uuid="123", entry=entry)
            >>> print(entry_uuid)
            "456"

        """
        response = self.http_client.do_request(
            "POST",
            f"/v1/datasets/{dataset_uuid}",
            json=entry.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to add entry with status {response.status_code}")
        return response.json()

    def get_entries(
        self, dataset_uuid: str, offset: int = 0, limit: int = 100
    ) -> List[DatasetEntryResponse]:
        """Get entries from a dataset

        This method retrieves entries from a specified dataset by its unique identifier. The entries are returned based on the specified offset and limit.

        Args:
            dataset_uuid (str): The unique identifier of the dataset.
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The maximum number of entries to retrieve. Defaults to 100.

        Returns:
            List[DatasetEntryResponseSchema]: A list of DatasetEntryResponseSchema instances representing the entries in the dataset.

        Raises:
            APIError: If the retrieval fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> entries = client.datasets.get_entries(dataset_uuid="123", offset=0, limit=10)
            >>> for entry in entries:
            ...     print(entry)
            DatasetEntryResponseSchema(uuid='456', input='Example input', output='Example output', ...)

        """
        response = self.http_client.do_request(
            "GET",
            f"/v1/datasets/{dataset_uuid}/entries",
            params={"offset": offset, "limit": limit},
        )
        if response.status_code != 200:
            raise APIError(f"Failed to get entries with status {response.status_code}")
        return [DatasetEntryResponse.model_validate(item) for item in response.json()]

    def get_entry(self, dataset_uuid: str, entry_uuid: str) -> DatasetEntryResponse:
        """Get a specific entry from a dataset

        This method retrieves a specific entry from a specified dataset by its unique identifier.

        Args:
            dataset_uuid (str): The unique identifier of the dataset.
            entry_uuid (str): The unique identifier of the entry.

        Returns:
            DatasetEntryResponseSchema: An instance of DatasetEntryResponseSchema representing the entry.

        Raises:
            APIError: If the retrieval fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> entry = client.datasets.get_entry(dataset_uuid="123", entry_uuid="456")
            >>> print(entry)
            DatasetEntryResponseSchema(uuid='456', input='Example input', output='Example output', ...)

        """
        response = self.http_client.do_request(
            "GET",
            f"/v1/datasets/{dataset_uuid}/entries/{entry_uuid}",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to get entry with status {response.status_code}")
        return DatasetEntryResponse.model_validate(response.json())

    def update_entry(
        self, dataset_uuid: str, entry_uuid: str, entry: DatasetEntryUpdate
    ) -> DatasetEntryResponse:
        """Update a specific entry in a dataset

        This method updates a specific entry in a specified dataset by its unique identifier.

        Args:
            dataset_uuid (str): The unique identifier of the dataset.
            entry_uuid (str): The unique identifier of the entry.
            entry (DatasetEntryUpdateSchema): The updated entry data.

        Returns:
            DatasetEntryResponseSchema: An instance of DatasetEntryResponseSchema representing the updated entry.

        Raises:
            APIError: If the update fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types.datasets import DatasetEntryUpdateSchema
            >>> client = Client(api_key="your_api_key_here")
            >>> updated_entry = DatasetEntryUpdateSchema(input="Updated input", output="Updated output")
            >>> entry = client.datasets.update_entry(dataset_uuid="123", entry_uuid="456", entry=updated_entry)
            >>> print(entry)
            DatasetEntryResponseSchema(uuid='456', input='Updated input', output='Updated output', ...)

        """
        response = self.http_client.do_request(
            "PUT",
            f"/v1/datasets/{dataset_uuid}/entries/{entry_uuid}",
            json=entry.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to update entry with status {response.status_code}")
        return DatasetEntryResponse.model_validate(response.json())

    def delete_entry(self, dataset_uuid: str, entry_uuid: str) -> bool:
        """Delete a specific entry from a dataset

        This method deletes a specific entry from a specified dataset by its unique identifier.

        Args:
            dataset_uuid (str): The unique identifier of the dataset.
            entry_uuid (str): The unique identifier of the entry.

        Returns:
            bool: True if the entry was successfully deleted, False otherwise.

        Raises:
            APIError: If the deletion fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> success = client.datasets.delete_entry(dataset_uuid="123", entry_uuid="456")
            >>> print(success)
            True

        """
        response = self.http_client.do_request(
            "DELETE",
            f"/v1/datasets/{dataset_uuid}/entries/{entry_uuid}",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to delete entry with status {response.status_code}")
        return response.json()
