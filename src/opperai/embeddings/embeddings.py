from dataclasses import dataclass
from typing import List, Optional, Union

from opperai._client import Client
from opperai.types import EmbeddingResponse


@dataclass
class Embeddings:
    _client: Client = None

    def __init__(self, client: Optional[Client] = None):
        if client is None:
            client = Client()

        self._client = client

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

        Examples:
            >>> from opperai import Opper
            >>> client = Opper()
            >>> response = client.embeddings.create(
            ...     model="text-embedding-ada-002",
            ...     input_text="Hello, world!"
            ... )
            >>> print(response.data[0])
            [0.0023064255, -0.009327292, ...]
        """
        return self._client.embeddings.create(
            model=model,
            input_text=input_text,
            encoding_format=encoding_format,
            user=user,
        )
