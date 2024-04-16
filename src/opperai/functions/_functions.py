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
        if path is not None:
            try:
                return self._delete_by_path(path)
            except APIError:
                pass
        elif id is not None:
            fn = self.get(id=id)
            if fn:
                return self._delete_by_path(fn.path)

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
