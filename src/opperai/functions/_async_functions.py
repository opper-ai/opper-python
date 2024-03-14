from typing import Generator

from opperai._http_clients import _async_http_client
from opperai.types import (
    ChatPayload,
    FunctionDescription,
    FunctionResponse,
    StreamingChunk,
    validate_id_xor_path,
)
from opperai.types.exceptions import APIError, RateLimitError


class AsyncFunctions:
    def __init__(self, http_client: _async_http_client, default_model: str = None):
        self.http_client = http_client
        self.default_model = default_model

    async def _create(self, function: FunctionDescription, **kwargs) -> int:
        response = await self.http_client.do_request(
            "POST",
            "/api/v1/functions",
            json=function.model_dump() | kwargs,
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to create function {function.path} with status {response.status_code}"
            )

        return response.json()["id"]

    async def update(self, function: FunctionDescription, **kwargs) -> int:
        response = await self.http_client.do_request(
            "POST",
            f"/api/v1/functions/{function.id}",
            json=function.model_dump() | kwargs,
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to update function {function.path} with status {response.status_code}"
            )

        return response.json()["id"]

    @validate_id_xor_path
    async def get(self, id: str = None, path: str = None) -> FunctionDescription | None:
        if path is not None:
            if id is not None:
                raise ValueError("Only one of id or path should be provided")
            return await self.get_by_path(path)
        elif id is not None:
            return await self.get_by_id(id)
        else:
            return None

    async def get_by_path(self, function_path: str) -> FunctionDescription | None:
        response = await self.http_client.do_request(
            "GET",
            f"/api/v1/functions/by_path/{function_path}",
        )
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise APIError(
                f"Failed to get function {function_path} with status {response.status_code}"
            )

        return FunctionDescription(**response.json())

    async def get_by_id(self, function_id: str) -> FunctionDescription | None:
        response = await self.http_client.do_request(
            "GET",
            f"/api/v1/functions/{function_id}",
        )
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise APIError(
                f"Failed to get function {function_id} with status {response.status_code}"
            )

        return FunctionDescription(**response.json())

    async def create(
        self, function: FunctionDescription, update: bool = True, **kwargs
    ) -> int | None:
        fn = await self.get_by_path(function.path)
        if fn is None:
            return await self._create(function, **kwargs)
        elif update:
            function.id = fn.id
            return await self.update(function, **kwargs)
        return fn.id

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
        if response.status_code != 200:
            raise APIError(
                f"Failed to delete function {function_path} with status {response.status_code}"
            )

    async def chat(
        self, function_path, data: ChatPayload, stream=False, **kwargs
    ) -> FunctionResponse:
        if stream:
            return self._chat_stream(function_path, data, **kwargs)
        serialized_data = data.model_dump()
        response = await self.http_client.do_request(
            "POST",
            f"/v1/chat/{function_path}",
            json=serialized_data | kwargs,
        )
        if response.status_code == 429:
            raise RateLimitError("Rate limit error: please retry in a few seconds")
        if response.status_code != 200:
            raise APIError(
                f"Failed to run function {function_path} with status {response.status_code}"
            )
        return FunctionResponse(**response.json())

    async def _chat_stream(
        self, function_path, data: ChatPayload, **kwargs
    ) -> Generator[StreamingChunk, None, None]:
        gen = self.http_client.stream(
            "POST",
            f"/v1/chat/{function_path}",
            json=data.model_dump() | kwargs,
            params={"stream": "True"},
        )
        async for item in gen:
            yield StreamingChunk(**item)
