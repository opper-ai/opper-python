from typing import List, Optional

from opperai.core._http_clients import _async_http_client
from opperai.core.spans import get_current_span_id
from opperai.types.exceptions import APIError, NotFoundError
from opperai.types.indexes import (
    Document,
    DocumentIn,
    Filter,
    Index,
    RetrievalResponse,
)

from ._indexes import RetrieveQuery


class AsyncIndexes:
    def __init__(self, http_client: _async_http_client):
        self.http_client = http_client

    async def create(
        self, name: str, embedding_model: str = "text-embedding-ada-002"
    ) -> Index:
        """Create an index

        This method sends a request to create a new index in the OpperAI service. If the index is successfully created, it returns an instance of the Index class representing the newly created index's configuration and details.

        Args:
            name (str): The name of the index to create.
            embedding_model (str, optional): The embedding model to use for indexing. Defaults to "text-embedding-ada-002".

        Returns:
            Index: An instance of the Index class representing the newly created index.

        Raises:
            APIError: If the index creation fails.

        Examples:
            >>> from opperai import AsyncClient
            >>> from opperai.exceptions import APIError
            >>> opper = AsyncClient(api_key="your-api-key")
            >>> index = asyncio.run(opper.indexes.create("my_index"))
            >>> print(index)
            Index(id='123', name='my_index', ...)

        """
        response = await self.http_client.do_request(
            "POST",
            "/v1/indexes",
            json={
                "name": name,
                "embedding_model": embedding_model,
            },
        )

        return Index.model_validate(response.json())

    async def get(
        self, uuid: Optional[str] = None, name: Optional[str] = None
    ) -> Optional[Index]:
        """Retrieve an index by UUID or name.

        Args:
            uuid (Optional[str], optional): The UUID of the index. Defaults to None.
            name (Optional[str], optional): The name of the index. Defaults to None.

        Raises:
            ValueError: If neither uuid nor name is provided, or if both are provided.
            APIError: If the retrieval fails.

        Returns:
            Optional[Index]: The retrieved index, or None if not found.
        """
        if uuid is None and name is None:
            raise ValueError("Either uuid or name must be provided")
        if uuid is not None and name is not None:
            raise ValueError("Only one of uuid or name should be provided")

        try:
            response = await self.http_client.do_request(
                "GET", f"/v1/indexes/{uuid if uuid else f'by-name/{name}'}"
            )
        except NotFoundError:
            return None

        return Index.model_validate(response.json())

    async def delete(
        self, uuid: Optional[str] = None, name: Optional[str] = None
    ) -> bool:
        """Delete an index by UUID or name.

        Args:
            uuid (Optional[str], optional): The UUID of the index. Defaults to None.
            name (Optional[str], optional): The name of the index. Defaults to None.

        Raises:
            ValueError: If neither uuid nor name is provided, or if both are provided.
            APIError: If the deletion fails.

        Returns:
            bool: True if deleted, False if not found.
        """
        if uuid is None and name is None:
            raise ValueError("Either uuid or name must be provided")
        if uuid is not None and name is not None:
            raise ValueError("Only one of uuid or name should be provided")

        try:
            await self.http_client.do_request(
                "DELETE", f"/v1/indexes/{uuid if uuid else f'by-name/{name}'}"
            )
        except NotFoundError:
            return False
        return True

    async def list(self) -> List[Index]:
        """List all indexes

        This method sends a GET request to the OpperAI service to retrieve a list of all indexes. It returns a list of Index instances, each representing an index's configuration and details.

        Returns:
            List[Index]: A list of Index instances representing all the indexes available.

        Raises:
            APIError: If the listing operation fails due to server-side issues.

        Examples:
            >>> from opperai import AsyncClient
            >>> opper = AsyncClient(api_key="your-api-key")
            >>> indexes = asyncio.run(opper.indexes.list())
            >>> for index in indexes:
            >>>     print(index)
        """
        response = await self.http_client.do_request(
            "GET",
            "/v1/indexes",
        )
        if response.status_code != 200:
            raise APIError(f"Failed to list indexes with status {response.status_code}")
        return [Index.model_validate(item) for item in response.json()]

    async def upload_file(self, uuid: str, file_path: str, **kwargs):
        """Upload a file to a specific index

        This method handles the uploading of a file to a specified index by first obtaining an upload URL, then uploading the file to that URL, and finally registering the file with the index.

        Args:
            uuid (str): The unique identifier of the index to which the file will be uploaded.
            file_path (str): The path to the file that needs to be uploaded.
            **kwargs: Additional parameters that can be passed to the register file API call.

        Returns:
            dict: A dictionary containing the response from the register file API call.

        Raises:
            APIError: If obtaining the upload URL, uploading the file, or registering the file fails.

        Examples:
            >>> from opperai import AsyncClient
            >>> opper = AsyncClient(api_key="your-api-key")
            >>> response = asyncio.run(opper.indexes.upload_file(123, "/path/to/file.txt"))
            >>> print(response)
        """
        # Get upload URL
        upload_url_response = await self.http_client.do_request(
            "GET",
            f"/v1/indexes/{uuid}/upload_url",
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
            f"/v1/indexes/{uuid}/register_file",
            json={"uuid": upload_url_data["uuid"], **kwargs},
        )
        if register_file_response.status_code != 200:
            raise APIError(
                f"Failed to register file with status {register_file_response.status_code}"
            )

        return register_file_response.json()

    async def upload_file_by_name(self, name: str, file_path: str, **kwargs):
        """Upload a file to an index specified by name

        This method handles the asynchronous uploading of a file to a specified index (identified
        by name) by first obtaining an upload URL, then uploading the file to that URL, and finally
        registering the file with the index.

        Args:
            name (str): The name of the index to which the file will be uploaded.
            file_path (str): The path to the file that needs to be uploaded.
            **kwargs: Additional parameters that can be passed to the register file API call.

        Returns:
            dict: A dictionary containing the response from the register file API call.

        Raises:
            APIError: If obtaining the upload URL, uploading the file, or registering the file fails.

        Examples:
            >>> from opperai import AsyncClient
            >>> client = AsyncClient(api_key="your_api_key_here")
            >>> response = await client.indexes.upload_file_by_name("my_index", "/path/to/file.txt")
            >>> print(response)
        """
        # Get upload URL
        upload_url_response = await self.http_client.do_request(
            "GET",
            f"/v1/indexes/upload_url/by-name/{name}",
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
            f"/v1/indexes/register_file/by-name/{name}",
            json={"uuid": upload_url_data["uuid"], **kwargs},
        )
        if register_file_response.status_code != 200:
            raise APIError(
                f"Failed to register file with status {register_file_response.status_code}"
            )

        return register_file_response.json()

    async def index(self, uuid: str, doc: DocumentIn) -> Document:
        """Index a document.

        This method sends a POST request to the OpperAI service to add a document to the specified index by its unique identifier. If the operation is successful, it returns the added document as an instance of the Document class.

        Args:
            id (int): The unique identifier of the index to which the document will be added.
            doc (Document): The document to be added to the index. It must be an instance of the Document class.

        Returns:
            Document: An instance of the Document class representing the added document.

        Raises:
            APIError: If the document addition fails for reasons such as the index not existing or the document being invalid.

        Examples:
            >>> from opperai import AsyncClient,
            >>> from opperai.types import Document
            >>> opper = AsyncClient(api_key="your-api-key")
            >>> doc = Document(id="doc1", content="This is a test document.")
            >>> added_doc = asyncio.run(opper.indexes.index(123, doc))
            >>> print(added_doc)
            Document(id='doc1', content='This is a test document.', ...)
        """
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/{uuid}/index",
            json=doc.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to add document with status {response.status_code}")
        return Document.model_validate(response.json())

    async def index_by_name(self, name: str, doc: Document) -> Document:
        """Index a document using the index name

        This method asynchronously adds a document to a specified index using the index's name.
        If the operation is successful, it returns the indexed document as a Document instance.

        Args:
            name (str): The name of the index where the document will be indexed.
            doc (Document): The document to be indexed. Must be an instance of Document.

        Returns:
            Document: An instance of the Document class representing the indexed document.

        Raises:
            APIError: If the document indexing fails due to reasons such as the index not existing
                     or the document being invalid.

        Examples:
            >>> from opperai import AsyncClient
            >>> from opperai.types.indexes import Document
            >>> client = AsyncClient(api_key="your_api_key_here")
            >>> doc = Document(content="Example content")
            >>> indexed_doc = await client.indexes.index_by_name("my_index", doc)
            >>> print(indexed_doc)
            Document(uuid='456', content='Example content', ...)
        """
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/index/by-name/{name}",
            json=doc.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(f"Failed to add document with status {response.status_code}")
        return Document.model_validate(response.json())

    async def retrieve(
        self,
        uuid: str,
        query: str,
        k: int,
        filters: Optional[List[Filter]] = None,
        parent_span_uuid: Optional[str] = None,
        **kwargs,
    ) -> List[RetrievalResponse]:
        """Retrieve documents

        This method sends a POST request to the OpperAI service to retrieve documents from the specified index. The documents are returned based on their relevance to the provided query string. The number of documents to return is specified by the `k` parameter. Optional filters can be applied to further refine the search results.

        Args:
            id (int): The unique identifier of the index from which documents will be retrieved.
            query (str): The query string used to search and retrieve relevant documents.
            k (int): The number of top relevant documents to retrieve.
            filters (Optional[List[Filter]], optional): A list of filters to apply to the query for refining results. Defaults to None.

        Returns:
            List[RetrievalResponse]: A list of RetrievalResponse objects, each representing a document that matches the query.

        Raises:
            APIError: If the retrieval operation fails for reasons such as the index not existing or the query being malformed.

        Examples:
            >>> from opperai import AsyncClient
            >>> from opperai.types import RetrievalResponse, Filter
            >>> opper = AsyncClient(api_key="your-api-key")
            >>> filters = [Filter(field="category", value="technology")]
            >>> responses = await opper.indexes.retrieve(id=123, query="latest tech trends", k=5, filters=filters)
            >>> for response in responses:
            >>>     print(response.document)
        """
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/{uuid}/query",
            json={
                **RetrieveQuery(
                    q=query,
                    k=k,
                    filters=filters,
                    parent_span_uuid=parent_span_uuid or get_current_span_id(),
                ).model_dump(),
                **kwargs,
            },
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to retrieve index {uuid} with status {response.status_code}"
            )
        return [RetrievalResponse.model_validate(item) for item in response.json()]

    async def retrieve_by_name(
        self,
        name: str,
        query: str,
        k: int,
        filters: Optional[List[Filter]] = None,
        parent_span_uuid: Optional[str] = None,
        **kwargs,
    ) -> List[RetrievalResponse]:
        """Retrieve documents using the index name

        This method asynchronously retrieves documents from a specified index based on a query,
        using the index's name instead of its UUID. It supports filtering and limiting the
        number of responses.

        Args:
            name (str): The name of the index from which to retrieve documents.
            query (str): The query string used to search and retrieve documents.
            k (int): The maximum number of documents to retrieve.
            filters (Optional[List[Filter]], optional): A list of filters to apply to the retrieval process.
            parent_span_uuid (Optional[str], optional): UUID of the parent span for tracing.
            **kwargs: Additional keyword arguments to pass to the query endpoint.

        Returns:
            List[RetrievalResponse]: A list of RetrievalResponse instances, each representing
            a document that matches the query criteria.

        Raises:
            APIError: If the retrieval process fails due to an API error.

        Examples:
            >>> from opperai import AsyncClient
            >>> from opperai.types.indexes import Filter
            >>> client = AsyncClient(api_key="your_api_key_here")
            >>> filters = [Filter(field="date", value="2021-01-01", operation="gte")]
            >>> responses = await client.indexes.retrieve_by_name(
            ...     name="my_index",
            ...     query="example query",
            ...     k=5,
            ...     filters=filters
            ... )
            >>> for response in responses:
            ...     print(response)
            RetrievalResponse(content='...', metadata={...})
        """
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/query/by-name/{name}",
            json={
                **RetrieveQuery(
                    q=query,
                    k=k,
                    filters=filters,
                    parent_span_uuid=parent_span_uuid or get_current_span_id(),
                ).model_dump(),
                **kwargs,
            },
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to retrieve index {name} with status {response.status_code}"
            )
        return [RetrievalResponse.model_validate(item) for item in response.json()]

    async def delete_by_name(self, name: str) -> bool:
        """Delete an index by name

        This method sends an asynchronous DELETE request to remove an index specified by its name.
        If the index does not exist, it returns False. If the deletion is successful, it returns True.

        Args:
            name (str): The name of the index to be deleted.

        Returns:
            bool: True if the index was successfully deleted, False if the index does not exist.

        Raises:
            APIError: If the deletion fails due to reasons other than the index not existing.

        Examples:
            >>> from opperai import AsyncClient
            >>> client = AsyncClient(api_key="your_api_key_here")
            >>> result = await client.indexes.delete_by_name("my_index")
            >>> print(result)
            True
        """
        try:
            await self.http_client.do_request(
                "DELETE",
                f"/v1/indexes/by-name/{name}",
            )
        except NotFoundError:
            return False
        return True
