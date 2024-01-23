from .types import ChatPayload, FunctionResponse, StreamingChunk
from typing import Generator


class Functions:
    def __init__(self, http_client):
        self.http_client = http_client

    def chat(
        self, function_path, data: ChatPayload, stream=False
    ) -> [FunctionResponse, Generator[StreamingChunk, None, None]]:
        if stream:
            return self._chat_stream(function_path, data)
        serialized_data = data.model_dump()

        data = self.http_client.do_request(
            "POST",
            f"/v1/chat/{function_path}",
            json=serialized_data,
        )
        return FunctionResponse(**data)

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


class AsyncFunctions:
    def __init__(self, http_client):
        self.http_client = http_client

    async def chat(
        self, function_path, data: ChatPayload, stream=False
    ) -> FunctionResponse:
        if stream:
            return self._chat_stream(function_path, data)
        serialized_data = data.model_dump()

        data = await self.http_client.do_request(
            "POST",
            f"/v1/chat/{function_path}",
            json=serialized_data,
            params={"stream": "true"} if stream else None,
        )
        return FunctionResponse(**data)

    async def _chat_stream(
        self,
        function_path,
        data: ChatPayload,
    ) -> FunctionResponse:
        gen = self.http_client.stream("POST", f"/v1/chat/{function_path}?stream=True")
        async for item in gen:
            yield StreamingChunk(**item)
