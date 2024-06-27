from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Union

from opperai._client import AsyncClient
from opperai.functions.decorator._schemas import type_to_json_schema
from opperai.types import ChatPayload, Message, StreamingChunk
from opperai.types import Function as FunctionModel
from opperai.types import FunctionResponse as FunctionResponseModel
from pydantic import PrivateAttr

from ..spans.async_spans import AsyncSpan


class AsyncFunctionResponse(FunctionResponseModel):
    _client: AsyncClient = PrivateAttr()

    def __init__(self, client: AsyncClient = None, **kwargs):
        super().__init__(**kwargs)
        if not client:
            client = AsyncClient()
        self._client = client

    @property
    def span(self):
        return AsyncSpan(self._client, self.span_id)


class AsyncStreamingResponse:
    _client: AsyncClient = None
    stream: Iterator[StreamingChunk] = None
    _context: Optional[List[Dict[str, Any]]] = None
    _span_id: Optional[str] = None

    def __init__(
        self, client: AsyncClient = None, stream: Iterator[StreamingChunk] = None
    ):
        if not client:
            client = AsyncClient()
        self._client = client
        self.stream = stream

    async def initialize(self):
        self.stream = await self.stream
        try:
            first_chunk = await self.stream.__anext__()
            self._span_id = (
                first_chunk.span_id if first_chunk.span_id is not None else None
            )
            self._context = (
                first_chunk.context if first_chunk.context is not None else []
            )
        except StopAsyncIteration:
            self._span_id = None
            self._context = []

    @property
    async def deltas(self):
        async for chunk in self.stream:
            if chunk.delta is not None:
                yield chunk.delta

    @property
    def span(self) -> AsyncSpan:
        return AsyncSpan(self._client, self._span_id)


@dataclass
class AsyncFunction:
    _client: AsyncClient
    _function: FunctionModel

    async def chat(
        self,
        messages: List[Message],
        parent_span_id: Optional[str] = None,
        stream: Optional[bool] = False,
    ) -> Union[AsyncFunctionResponse, AsyncStreamingResponse]:
        if stream:
            if self._function.out_schema is not None:
                raise ValueError(
                    "Cannot stream output for functions structured response"
                )

            response = self._client.functions.chat(
                function_path=self._function.path,
                data=ChatPayload(messages=messages, parent_span_uuid=parent_span_id),
                stream=stream,
            )

            res = AsyncStreamingResponse(client=self._client, stream=response)
            await res.initialize()
            return res

        response: FunctionResponseModel = await self._client.functions.chat(
            function_path=self._function.path,
            data=ChatPayload(messages=messages, parent_span_uuid=parent_span_id),
            stream=stream,
        )

        return AsyncFunctionResponse(client=self._client, **response.model_dump())

    async def delete(self) -> bool:
        return await self._client.functions.delete(uuid=self._function.uuid)

    async def flush_cache(self) -> bool:
        return await self._client.functions.flush_cache(uuid=self._function.uuid)

    async def update(self, **kwargs) -> "AsyncFunction":
        updated = self._function.model_dump(exclude_none=True)
        kwargs["input_schema"] = None
        kwargs["out_schema"] = None
        if "input_type" in kwargs and kwargs["input_type"] is not None:
            kwargs["input_schema"] = type_to_json_schema(kwargs["input_type"])
            del kwargs["input_type"]
        if "output_type" in kwargs and kwargs["output_type"] is not None:
            kwargs["out_schema"] = type_to_json_schema(kwargs["output_type"])
            del kwargs["output_type"]

        for key, value in kwargs.items():
            updated[key] = value

        updated_model = FunctionModel.model_validate(updated)
        updated_function = await self._client.functions.update(
            uuid=self._function.uuid, function=updated_model
        )
        self._function = updated_function

        return self


@dataclass
class AsyncFunctions:
    _client: AsyncClient = None

    def __init__(self, client: AsyncClient = None):
        if client is None:
            client = AsyncClient()

        self._client = client

    async def create(
        self,
        path: str,
        instructions: str,
        description: Optional[str] = None,
        input_type: Optional[Any] = None,
        output_type: Optional[Any] = None,
        model: Optional[str] = None,
    ) -> AsyncFunction:
        try:
            function = await self.get(path=path)
            if function:
                return await function.update(
                    instructions=instructions,
                    description=description,
                    input_type=input_type,
                    output_type=output_type,
                    model=model,
                )
        except Exception:
            pass

        if input_type:
            input_schema = type_to_json_schema(input_type)
        if output_type:
            output_schema = type_to_json_schema(output_type)

        function = await self._client.functions.create(
            FunctionModel(
                path=path,
                instructions=instructions,
                description=description,
                input_schema=input_schema if input_type else None,
                out_schema=output_schema if output_type else None,
                model=model,
            )
        )

        return AsyncFunction(self._client, function)

    async def get(self, uuid: str = None, path: str = None) -> Optional[AsyncFunction]:
        if uuid is not None:
            function = await self._client.functions.get(uuid=uuid)
        elif path is not None:
            function = await self._client.functions.get(path=path)
        else:
            raise ValueError("Either id or name must be provided")

        if not function:
            return None

        return AsyncFunction(self._client, function)

    async def delete(self, uuid: str = None, path: str = None) -> bool:
        if uuid is not None:
            return await self._client.functions.delete(uuid=uuid)
        elif path is not None:
            return await self._client.functions.delete(path=path)
        else:
            raise ValueError("Either id or name must be provided")
