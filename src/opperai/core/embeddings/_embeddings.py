from http import HTTPStatus
from typing import List, Optional, Union

from opperai.core._http_clients import _http_client
from opperai.types import EmbeddingRequest, EmbeddingResponse
from opperai.types.exceptions import APIError


class Embeddings:
    def __init__(self, http_client: _http_client):
        self.http_client = http_client

    def create(
        self,
        model: str,
        input_text: Union[str, List[str]],
        encoding_format: Optional[str] = None,
        user: Optional[str] = None,
    ) -> EmbeddingResponse:
        """Create embeddings for the given input text.

        Args:
            model (str): The ID of the model to use for generating embeddings.
            input_text (Union[str, List[str]]): The input text to obtain embeddings for.
                This can be a single string or a list of strings.
            encoding_format (str, optional): The format for the embedding vector data.
                Defaults to None.
            user (str, optional): A unique identifier for the end-user. Defaults to None.

        Returns:
            EmbeddingResponse: An object containing the generated embeddings.

        Raises:
            APIError: If the embeddings creation fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> response = client.embeddings.create(
            ...     model="text-embedding-ada-002",
            ...     input_text="Hello, world!"
            ... )
            >>> print(response.data[0])
            [0.0023064255, -0.009327292, ...]
        """
        request = EmbeddingRequest(
            model=model,
            input=input_text,
            encoding_format=encoding_format,
            user=user,
        )

        response = self.http_client.do_request(
            "POST",
            "/v1/embeddings",
            json=request.model_dump(exclude_none=True),
        )

        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to create embeddings with status {response.status_code}: {response.text}"
            )

        return EmbeddingResponse.model_validate(response.json())
