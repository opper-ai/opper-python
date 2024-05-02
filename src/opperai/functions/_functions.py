from typing import Generator, Optional

from opperai._http_clients import _http_client
from opperai.spans import get_current_span_id
from opperai.types import (
    ChatPayload,
    Function,
    FunctionResponse,
    StreamingChunk,
    validate_id_xor_path,
)
from http import HTTPStatus
from opperai.types.exceptions import (
    APIError,
    RateLimitError,
    StructuredGenerationError,
)


class Functions:
    def __init__(self, http_client: _http_client, default_model: str = None):
        self.http_client = http_client
        self.default_model = default_model

    def create(self, function: Function, update: bool = True, **kwargs) -> Function:
        """
        Create a function

        This method allows for the creation or updating of a function based on the provided Function instance. If the function does not exist, it will be created. If it does exist and the update parameter is set to True, the function will be updated.

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

        Examples:
            >>> from opperai import Client
            >>> from opperai.types import Function
            >>> client = Client(api_key="your_api_key_here")
            >>> function = Function(
            ...     path="example/function",
            ...     description="A function to do something",
            ...     model="gpt-3.5-turbo"
            ... )
            >>> created_function = client.functions.create(function)
            >>> print(created_function)
            Function(id='123', path='example/function', description='A function to do something', model='gpt-3.5-turbo')

            >>> # Using a decorator:
            >>> from opperai import fn
            >>>
            >>> @fn(path="test/test", model="openai/gpt4-turbo")
            >>> def translate(text=str) -> str:
            >>>     ''' Translate the given text to French'''
            >>> print(translate("This is a text"))
            'Ceci est un texte'
        """
        fn = self.get(path=function.path)
        if fn is None:
            return self._create(function, **kwargs)
        elif update:
            function.id = fn.id
            return self.update(function, **kwargs)
        else:
            return fn

    def _create(self, function: Function, **kwargs) -> Function:
        if not function.model and self.default_model:
            function.model = self.default_model
        response = self.http_client.do_request(
            "POST",
            "/api/v1/functions",
            json={**function.model_dump(), **kwargs},
        )
        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to create function {function.path} with status {response.status_code}: {response.text}"
            )

        return Function.model_validate(response.json())

    def update(self, function: Function, **kwargs) -> Function:
        """
        Update a function

        This method updates an existing function based on the provided Function instance. The function to be updated is identified by its unique ID, which must be set in the Function instance.

        Args:
            function (Function): An instance of the Function class, representing the updated configuration
                of the function. This includes details such as the function's model, path, description, and any other relevant configuration parameters.
            **kwargs: Additional keyword arguments that will be included in the request payload.

        Returns:
            Function: An instance of the Function class, representing the updated function, including its server-assigned ID and any other relevant information.

        Raises:
            APIError: If the function update fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types import Function
            >>> client = Client(api_key="your_api_key_here")
            >>> function = Function(
            ...     id='123',
            ...     path="example/function",
            ...     description="An updated description",
            ...     model="gpt-3.5-turbo"
            ... )
            >>> updated_function = client.functions.update(function)
            >>> print(updated_function)
            Function(id='123', path='example/function', description='An updated description', model='gpt-3.5-turbo')
        """
        response = self.http_client.do_request(
            "POST",
            f"/api/v1/functions/{function.id}",
            json={**function.model_dump(), **kwargs},
        )
        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to update function `{function.path}` with status {response.status_code}: {response.text}"
            )

        return Function.model_validate(response.json())

    @validate_id_xor_path
    def get(self, id: str = None, path: str = None) -> Optional[Function]:
        """
        Get a function

        This method allows fetching the details of a specific Opper function, either by specifying its unique ID or its path. If the function is found, it returns an instance of the Function class representing the function's configuration and details. If no function matches the given ID or path, or if both parameters are omitted, None is returned.

        Args:
            id (str, optional): The unique identifier of the function to retrieve. Defaults to None.
            path (str, optional): The path of the function to retrieve. Defaults to None.

        Returns:
            Optional[Function]: An instance of the Function class if the function is found, otherwise None.

        Raises:
            ValueError: If both `id` and `path` are provided, indicating ambiguous parameters.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> function_by_id = client.functions.get(id="123")
            >>> print(function_by_id)
            Function(id='123', path='example/function', ...)

            >>> function_by_path = client.functions.get(path="example/function")
            >>> print(function_by_path)
            Function(id='123', path='example/function', ...)

        Note:
            It is recommended to provide either `id` or `path`, but not both, to avoid ambiguity. If neither is provided, the method will return None.
        """
        if path is not None:
            if id is not None:
                raise ValueError("Only one of id or path should be provided")
            return self._get_by_path(path)
        elif id is not None:
            return self._get_by_id(id)
        else:
            return None

    def _get_by_path(self, function_path: str) -> Optional[Function]:
        response = self.http_client.do_request(
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

    def _get_by_id(self, function_id: str) -> Optional[Function]:
        response = self.http_client.do_request(
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

    @validate_id_xor_path
    def delete(self, id: str = None, path: str = None) -> bool:
        """
        Delete a function

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
            >>> from opperai import Client
            >>> client = Client(api_key="opper_api_key")
            >>> response = client.functions.delete(path="test/function")
            >>> print(response)
            True

        Note:
            It's important to provide either `id` or `path`, but not both. If neither is provided, the method
            will raise a ValueError to indicate the issue.
        """
        if path is not None:
            try:
                return self._delete_by_path(path)
            except APIError:
                pass
        elif id is not None:
            fn = self.get(id=id)
            if fn:
                return self._delete_by_path(fn.path)
        return False

    def _delete_by_path(self, function_path: str) -> bool:
        response = self.http_client.do_request(
            "DELETE",
            f"/api/v1/functions/by_path/{function_path}",
        )
        if response.status_code != HTTPStatus.OK:
            raise APIError(
                f"Failed to delete function {function_path} with status {response.status_code}"
            )
        return True

    def chat(
        self, function_path, data: ChatPayload, stream=False, **kwargs
    ) -> [FunctionResponse, Generator[StreamingChunk, None, None]]:
        if data.parent_span_uuid is None:
            data.parent_span_uuid = get_current_span_id()

        if stream:
            return self._chat_stream(function_path, data, **kwargs)
        serialized_data = data.model_dump()
        response = self.http_client.do_request(
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

    def _chat_stream(
        self, function_path, data: ChatPayload, **kwargs
    ) -> Generator[StreamingChunk, None, None]:
        serialized_data = data.model_dump()
        gen = self.http_client.stream(
            "POST",
            f"/v1/chat/{function_path}",
            json={**serialized_data, **kwargs},
            params={"stream": "True"},
        )
        for item in gen:
            yield StreamingChunk(**item)

    def flush_cache(self, id: int) -> bool:
        response = self.http_client.do_request(
            "DELETE",
            f"/api/v1/functions/{id}/cache",
        )
        if response.status_code != HTTPStatus.NO_CONTENT:
            raise APIError(
                f"Failed to flush cache for function with id={id} with status {response.status_code}"
            )

        return True
