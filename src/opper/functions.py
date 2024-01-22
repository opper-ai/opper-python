from .types import ChatPayload, FunctionResponse


class Functions:
    def __init__(self, http_client):
        self.http_client = http_client

    def chat(self, function_path, data: ChatPayload, stream=False) -> FunctionResponse:
        serialized_data = data.model_dump()

        data = self.http_client.do_request(
            "POST",
            f"/v1/chat/{function_path}",
            json=serialized_data,
            params={"stream": "true"} if stream else None,
        )
        return FunctionResponse(**data)


class AsyncFunctions:
    def __init__(self, http_client):
        self.http_client = http_client

    async def chat(
        self, function_path, data: ChatPayload, stream=False
    ) -> FunctionResponse:
        serialized_data = data.model_dump()

        data = await self.http_client.do_request(
            "POST",
            f"/v1/chat/{function_path}",
            json=serialized_data,
            params={"stream": "true"} if stream else None,
        )
        return FunctionResponse(**data)
