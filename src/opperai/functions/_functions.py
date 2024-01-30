from typing import Generator

from opperai._http_clients import _http_client
from opperai.types import (
    ChatPayload,
    FunctionDescription,
    FunctionResponse,
    StreamingChunk,
)
from opperai.types.exceptions import APIError


class Functions:
    def __init__(self, http_client: _http_client):
        self.http_client = http_client

    def _create_function(self, function: FunctionDescription) -> int:
        response = self.http_client.do_request(
            "POST",
            "/api/v1/functions",
            json=function.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to create function {function.path} with status {response.status_code}"
            )
        return response.json()["id"]

    def update_function(self, function: FunctionDescription) -> int:
        response = self.http_client.do_request(
            "POST",
            f"/api/v1/functions/{function.id}",
            json=function.model_dump(),
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to update function `{function.path}` with status {response.status_code}"
            )
        return response.json()["id"]

    def get_function_by_path(self, function_path: str) -> FunctionDescription:
        response = self.http_client.do_request(
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

    def get_function_by_id(self, function_id: str) -> FunctionDescription:
        response = self.http_client.do_request(
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

    def create_function(
        self, function: FunctionDescription, update: bool = True
    ) -> int:
        f = self.get_function_by_path(function.path)
        if f is None:
            return self._create_function(function)
        elif update:
            function.id = f.id
            return self.update_function(function)
        return None

    def chat(
        self, function_path, data: ChatPayload, stream=False
    ) -> [FunctionResponse, Generator[StreamingChunk, None, None]]:
        if stream:
            return self._chat_stream(function_path, data)
        serialized_data = data.model_dump()
        response = self.http_client.do_request(
            "POST",
            f"/v1/chat/{function_path}",
            json=serialized_data,
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to run function {function_path} with status {response.status_code}"
            )
        return FunctionResponse(**response.json())

    def _chat_stream(
        self,
        function_path,
        data: ChatPayload,
    ) -> Generator[StreamingChunk, None, None]:
        serialized_data = data.model_dump()
        gen = self.http_client.stream(
            "POST",
            f"/v1/chat/{function_path}?stream=True",
            json=serialized_data,
            params={"stream": "True"},
        )
        for item in gen:
            yield StreamingChunk(**item)
