from typing import List, Optional

from opperai.core._http_clients import _http_client
from opperai.types.exceptions import APIError
from opperai.types.indexes import (
    Document,
    Filter,
    Index,
    RetrievalResponse,
)
from pydantic import BaseModel, Field


class RetrieveQuery(BaseModel):
    q: str = Field(description="Query string")
    k: int = Field(default=3, description="Number of documents to retrieve")
    filters: Optional[List[Filter]] = Field(
        default=None, description="Filters to apply"
    )


class Indexes:
    def __init__(self, http_client: _http_client):
        self.http_client = http_client

    def create(self, name: str) -> Index:
        """Create an index

        This method allows for the creation of an index with the specified name. If the creation is successful, it returns an instance of the Index class, representing the newly created index.

        Args:
            name (str): The name of the index to be created.

        Returns:
            Index: An instance of the Index class, representing the newly created index.

        Raises:
            APIError: If the index creation fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> index = client.indexes.create(name="my_new_index")
            >>> print(index)
            Index(id='123', name='my_new_index')

        """
        response = self.http_client.do_request(
            "POST",
            "/v1/indexes",
            json={"name": name},
        )
        if response.status_code != 200:
            raise APIError(f"Failed to create index with status {response.status_code}")
        return Index.model_validate(response.json())

    def delete(self, id: int) -> bool:
        """Delete an index

        This method allows for the deletion of an index by specifying its unique identifier. If the deletion is successful, the method returns True. If the index cannot be found or the deletion fails, the method returns False.

        Args:
            id (int): The unique identifier of the index to delete.

        Returns:
            bool: True if the index was successfully deleted, False otherwise.

        Raises:
            APIError: If the index deletion fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> response = client.indexes.delete(id=123)
            >>> print(response)
            True

        """
        response = self.http_client.do_request(
            "DELETE",
            f"/v1/indexes/{id}",
        )
        if response.status_code == 404:
            return False
        if response.status_code != 200:
            raise APIError(f"Failed to delete index with status {response.status_code}")
        return True

    def get(self, id: int = None, name: str = None) -> Optional[Index]:
        """Retrieve an index

        This method fetches an index either by its unique identifier or by its name. If the index is found, it returns an instance of the Index class representing the index's details. If no index matches the given ID or name, or if both parameters are omitted, None is returned.

        Args:
            id (int, optional): The unique identifier of the index to retrieve. Defaults to None.
            name (str, optional): The name of the index to retrieve. Defaults to None.

        Returns:
            Optional[Index]: An instance of the Index class if the index is found, otherwise None.

        Raises:
            ValueError: If both `id` and `name` are provided, indicating ambiguous parameters.
            APIError: If the retrieval fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> index_by_id = client.indexes.get(id=123)
            >>> print(index_by_id)
            Index(id='123', name='my_index', ...)

            >>> index_by_name = client.indexes.get(name="my_index")
            >>> print(index_by_name)
            Index(id='123', name='my_index', ...)

        Note:
            It is recommended to provide either `id` or `name`, but not both, to avoid ambiguity. If neither is provided, the method will return None.
        """
        if id is None and name is None:
            raise ValueError("Either id or name must be provided")
        if id is not None and name is not None:
            raise ValueError("Only one of id or name should be provided")

        if id is not None:
            return self._get_by_id(id)
        if name is not None:
            return self._get_by_name(name)

    def _get_by_id(self, id: int) -> Optional[Index]:
        response = self.http_client.do_request(
            "GET",
            f"/v1/indexes/{id}",
        )
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise APIError(f"Failed to get index with status {response.status_code}")

        return Index.model_validate(response.json())

    def _get_by_name(self, name: str) -> Optional[Index]:
        indexes = self.list()
        for index in indexes:
            if index.name == name:
                return index
        return None

    def list(self) -> List[Index]:
        """List all indexes

        This method retrieves a list of all indexes available in the system. It returns a list of Index instances, each representing the details of an index.

        Returns:
            List[Index]: A list of Index instances representing all the indexes available.

        Raises:
            APIError: If the listing of indexes fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> indexes = client.indexes.list()
            >>> for index in indexes:
            ...     print(index)
            Index(id='123', name='my_index', ...)
            Index(id='124', name='another_index', ...)

        """
        response = self.http_client.do_request(
            "GET",
            "/v1/indexes",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to list indexes with status {response.status_code}")
        return [Index.model_validate(item) for item in response.json()]

    def upload_file(self, id: int, file_path: str, **kwargs):
        """Upload a file to an index

        This method uploads a file to a specified index by its unique identifier. The file is uploaded to a pre-signed URL obtained from the server, and then the file is registered with the index.

        Args:
            id (int): The unique identifier of the index to which the file is being uploaded.
            file_path (str): The path to the file that needs to be uploaded.
            **kwargs: Additional keyword arguments that will be included in the registration request.

        Returns:
            dict: A dictionary containing the server's response to the file registration.

        Raises:
            APIError: If the file upload or registration fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> response = client.indexes.upload_file(id=123, file_path="/path/to/file.txt")
            >>> print(response)
            {'message': 'File uploaded and registered successfully'}

        """
        # Get upload URL
        upload_url_response = self.http_client.do_request(
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
            upload_response = self.http_client.do_request(
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
        register_file_response = self.http_client.do_request(
            "POST",
            f"/v1/indexes/{id}/register_file",
            json={"uuid": upload_url_data["uuid"], **kwargs},
        )
        if register_file_response.status_code != 200:
            raise APIError(
                f"Failed to register file with status {register_file_response.status_code}"
            )

        return register_file_response.json()

    def index(self, id: int, doc: Document) -> Document:
        """Index a document

        This method adds a document to a specified index by its unique identifier. The document is indexed within the system, making it searchable or retrievable according to the index's configuration.

        Args:
            id (int): The unique identifier of the index where the document will be indexed.
            doc (Document): The document to be indexed.

        Returns:
            Document: An instance of the Document class, representing the indexed document with any server-assigned metadata.

        Raises:
            APIError: If the document indexing fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types.indexes import Document
            >>> client = Client(api_key="your_api_key_here")
            >>> doc = Document(content="Example content")
            >>> indexed_doc = client.indexes.index(id=123, doc=doc)
            >>> print(indexed_doc)
            Document(id='456', content='Example content', ...)

        """
        response = self.http_client.do_request(
            "POST",
            f"/v1/indexes/{id}/index",
            json=doc.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to add document with status {response.status_code}")
        return Document.model_validate(response.json())

    def retrieve(
        self,
        id: int,
        query: str,
        k: int,
        filters: Optional[List[Filter]] = None,
        **kwargs,
    ) -> List[RetrievalResponse]:
        """Retrieve documents from an index

        This method retrieves documents from a specified index based on a query. It supports filtering and limiting the number of responses.

        Args:
            id (int): The unique identifier of the index from which documents are to be retrieved.
            query (str): The query string used to search and retrieve documents.
            k (int): The maximum number of documents to retrieve.
            filters (Optional[List[Filter]], optional): A list of filters to apply to the retrieval process.

        Returns:
            List[RetrievalResponse]: A list of RetrievalResponse instances, each representing a document that matches the query criteria.

        Raises:
            APIError: If the retrieval process fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types.indexes import Filter
            >>> client = Client(api_key="your_api_key_here")
            >>> filters = [Filter(field="date", value="2021-01-01", operation="gte")]
            >>> responses = client.indexes.retrieve(id=123, query="example query", k=5, filters=filters)
            >>> for response in responses:
            ...     print(response)
            RetrievalResponse(id='doc123', score=0.98, ...)

        """
        response = self.http_client.do_request(
            "POST",
            f"/v1/indexes/{id}/query",
            json={
                **RetrieveQuery(q=query, k=k, filters=filters).model_dump(),
                **kwargs,
            },
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to retrieve index {id} with status {response.status_code}"
            )
        return [RetrievalResponse.model_validate(item) for item in response.json()]
