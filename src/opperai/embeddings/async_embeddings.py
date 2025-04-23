from dataclasses import dataclass
from typing import List, Optional, Union

from opperai._client import AsyncClient
from opperai.types import EmbeddingResponse


@dataclass
class AsyncEmbeddings:
    _client: AsyncClient = None

    def __init__(self, client: Optional[AsyncClient] = None):
        if client is None:
            client = AsyncClient()

        self._client = client

    async def create(
        self,
        model: str,
        input_text: Union[str, List[str]],
        encoding_format: Optional[str] = None,
        user: Optional[str] = None,
    ) -> EmbeddingResponse:
        """Create embeddings for the given input text asynchronously.

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
            >>> from opperai import AsyncOpper
            >>> client = AsyncOpper()
            >>> response = await client.embeddings.create(
            ...     model="text-embedding-ada-002",
            ...     input_text="Hello, world!"
            ... )
            >>> print(response.data[0])
            [0.0023064255, -0.009327292, ...]
        """
        return await self._client.embeddings.create(
            model=model,
            input_text=input_text,
            encoding_format=encoding_format,
            user=user,
        )
