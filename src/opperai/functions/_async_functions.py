from typing import Generator, Optional

from opperai._http_clients import _async_http_client
from opperai.spans import get_current_span_id
from opperai.types import (
    ChatPayload,
    Function,
    FunctionResponse,
    StreamingChunk,
    validate_id_xor_path,
)
from http import HTTPStatus
from opperai.types.exceptions import APIError, RateLimitError, StructuredGenerationError


class AsyncFunctions:
    def __init__(self, http_client: _async_http_client, default_model: str = None):
        self.http_client = http_client
        self.default_model = default_model

    async def _create(self, function: Function, **kwargs) -> Function:
        if not function.model and self.default_model:
            function.model = self.default_model
        response = await self.http_client.do_request(
            "POST",
            "/api/v1/functions",
            json={**function.model_dump(), **kwargs},
        )
        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to create function {function.path} with status {response.status_code}"
            )

        return Function.model_validate(response.json())

    async def update(self, function: Function, **kwargs) -> Function:
        response = await self.http_client.do_request(
            "POST",
            f"/api/v1/functions/{function.id}",
            json={**function.model_dump(), **kwargs},
        )
        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to update function {function.path} with status {response.status_code}"
            )

        return Function.model_validate(response.json())

    @validate_id_xor_path
    async def get(self, id: str = None, path: str = None) -> Optional[Function]:
        if path is not None:
            if id is not None:
                raise ValueError("Only one of id or path should be provided")
            return await self._get_by_path(path)
        elif id is not None:
            return await self._get_by_id(id)
        else:
            return None

    async def _get_by_path(self, function_path: str) -> Function:
        response = await self.http_client.do_request(
            "GET",
            f"/api/v1/functions/by_path/{function_path}",
        )
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None
        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to get function {function_path} with status {response.status_code}"
            )

        return Function.model_validate(response.json())

    async def _get_by_id(self, function_id: str) -> Function:
        response = await self.http_client.do_request(
            "GET",
            f"/api/v1/functions/{function_id}",
        )
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None
        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to get function {function_id} with status {response.status_code}"
            )

        return Function.model_validate(response.json())

    async def create(
        self, function: Function, update: bool = True, **kwargs
    ) -> Function:
        """ Create or update an Opper function.

        Args:
            function (Function): An instance of the Function class, representing the configuration
                of the function to be created or updated. This includes details such as the function's
                model, path, description, and any other relevant configuration parameters.
            update (bool, optional): If True, the function will be updated if it already exists
                based on its path. Defaults to True.
            **kwargs: Additional keyword arguments that will be included in the request payload.

        Returns:
            Function: An instance of the Function class, representing the newly created or updated
                function, including its server-assigned ID and any other relevant information.

        Raises:
            APIError: If the function creation or update fails due to an API error.
            ValueError: If both `id` and `path` are provided, or neither is provided.

        Examples:
            >>> from opperai import AsyncClient
            >>> from opperai.types import Function
            >>> client = AsyncClient(api_key="your_api_key_here")
            >>> function = Function(
            ...     path="example/function",
            ...     description="A function to do something",
            ...     model="gpt-3.5-turbo"
            ... )
            >>> created_function = asyncio.run(client.functions.create(function))
            >>> print(created_function)
            
            id=93 path='test/function' description='A function to translate text to French' input_schema=None out_schema=None instructions='Translate the given text to French.' model='azure/gpt4-eu' index_ids=[] use_semantic_search=None few_shot=False few_shot_count=2 cache_configuration=None
        """
        fn = await self.get(path=function.path)
        if fn is None:
            return await self._create(function, **kwargs)
        elif update:
            function.id = fn.id
            return await self.update(function, **kwargs)
        return fn

    @validate_id_xor_path
    async def delete(self, id: str = None, path: str = None):
        """ Delete an Opper function by its ID or path.

        This method allows for the deletion of a function either by specifying its unique ID or its path. 
        If the deletion is successful, the method returns True. If the function cannot be found or the deletion 
        fails, the method returns False.

        Args:
            id (str, optional): The unique identifier of the function to delete. Defaults to None.
            path (str, optional): The path of the function to delete. Defaults to None.

        Returns:
            bool: True if the function was successfully deleted, False otherwise.

        Raises:
            ValueError: If both `id` and `path` are provided, or if neither is provided.

        Examples:
            >>> from opperai import AsyncClient

            >>> client = AsyncClient(api_key="opper_api_key")
            >>> response = asyncio.run(client.functions.delete(path="test/function"))
            >>> print(response)
            True

        Note:
            It's important to provide either `id` or `path`, but not both. If neither is provided, the method 
            will raise a ValueError to indicate the issue.
        """
        
        if path is not None:
            try:
                await self._delete_by_path(path)
            except APIError:
                pass
        elif id is not None:
            fn = await self.get(id=id)
            if fn:
                await self._delete_by_path(fn.path)

    async def _delete_by_path(self, function_path: str):
        response = await self.http_client.do_request(
            "DELETE",
            f"/api/v1/functions/by_path/{function_path}",
        )
        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to delete function {function_path} with status {response.status_code}"
            )

    async def chat(
        self, function_path, data: ChatPayload, stream=False, **kwargs
    ) -> FunctionResponse:
        """ Send messages to a specific Opper function and receive a response.

        This method allows sending a message or a series of messages to a specified Opper function,
        identified by its path. The function processes the message(s) and returns a response. This
        method can operate in two modes: default and streaming. In default mode, it sends all messages
        and waits for a single response. In streaming mode, it yields incremental results as they become
        available.

        Args:
            function_path (str): The path identifier for the target Opper function. This should be
                obtained through the app interface or API.
            data (ChatPayload): An object of type ChatPayload, representing the content to be processed
                during the interaction. It encapsulates the messages to be sent to the function.
            stream (bool, optional): When set to True, initializes a generator that yields incremental
                results as StreamingChunk objects. Defaults to False for single message exchanges.
            **kwargs: Additional keyword arguments that will be passed to the underlying HTTP request.

        Returns:
            Union[FunctionResponse, Generator[StreamingChunk, None, None]]: By default, returns a
            FunctionResponse object containing the function's response to the input messages. If
            `stream` is True, it yields a generator of StreamingChunk objects, each representing a
            portion of the function's response.

        Examples:
            >>> import asyncio
            >>> from opperai import AsyncClient
            >>> from opperai.types import ChatPayload, Message

            >>> client = AsyncClient(api_key="your_api_key_here")

            >>> response = asyncio.run(client.functions.chat(
            ...    "test/function",
            ...    ChatPayload(
            ...        messages=[Message(role="user", content="hello")]
            ...    )
            ... ))
            >>> print(response.message)
            'Bonjour'

            # Example with streaming
            >>> async def stream_chat():
            ...     async for chunk in client.functions.chat(
            ...         "test/function",
            ...         ChatPayload(messages=[Message(role="user", content="hello")]),
            ...         stream=True
            ...     ):
            ...         print(chunk.message)
            >>> asyncio.run(stream_chat())

        Note:
            The `stream` parameter allows for real-time interaction with the function, which can be
            particularly useful for functions designed to process input incrementally or maintain a
            conversation state.
        """

        if data.parent_span_uuid is None:
            data.parent_span_uuid = get_current_span_id()
        if stream:
            return self._chat_stream(function_path, data, **kwargs)
        serialized_data = data.model_dump()
        response = await self.http_client.do_request(
            "POST",
            f"/v1/chat/{function_path}",
            json={**serialized_data, **kwargs},
        )

        if response.status_code == HTTPStatus.OK:
            return FunctionResponse.model_validate(response.json())
        elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitError("Rate limit error: please retry in a few seconds")
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            raise StructuredGenerationError(response.text)

        raise APIError(
            f"Failed to run function {function_path} with status {response.status_code}"
        )

    async def _chat_stream(
        self, function_path, data: ChatPayload, **kwargs
    ) -> Generator[StreamingChunk, None, None]:
        gen = self.http_client.stream(
            "POST",
            f"/v1/chat/{function_path}",
            json={**data.model_dump(), **kwargs},
            params={"stream": "True"},
        )
        async for item in gen:
            yield StreamingChunk(**item)

    async def flush_cache(self, id: int) -> None:
        response = await self.http_client.do_request(
            "DELETE",
            f"/api/v1/functions/{id}/cache",
        )
        if response.status_code != HTTPStatus.NO_CONTENT:
            raise APIError(
                f"Failed to flush cache for function with id={id} with status {response.status_code}"
            )
