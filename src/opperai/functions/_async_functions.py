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
        fn = await self.get(path=function.path)
        if fn is None:
            return await self._create(function, **kwargs)
        elif update:
            function.id = fn.id
            return await self.update(function, **kwargs)
        return fn

    @validate_id_xor_path
    async def delete(self, id: str = None, path: str = None):
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
