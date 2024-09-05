import inspect
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
    get_args,
    get_origin,
)

from opperai._client import AsyncClient
from opperai.datasets.async_datasets import AsyncDataset
from opperai.functions.decorator._schemas import type_to_json_schema
from opperai.types import (
    CallConfiguration,
    CallPayload,
    ChatPayload,
    Example,
    ImageOutput,
    Message,
    StreamingChunk,
)
from opperai.types import Function as FunctionModel
from opperai.types import FunctionResponse as FunctionResponseModel
from pydantic import BaseModel, PrivateAttr

from ..spans.async_spans import AsyncSpan
from .functions import T, djb2, prepare_input


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

    async def call(
        self,
        input: Any = None,
        examples: Optional[List[Example]] = None,
        configuration: Optional[CallConfiguration] = None,
    ) -> Tuple[T, AsyncFunctionResponse]:
        payload = CallPayload(
            input=input,
            examples=examples,
        )
        if configuration:
            payload.configuration = configuration

        return await self._client.functions.call(
            uuid=self._function.uuid,
            payload=payload,
        )

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

    def dataset(self) -> AsyncDataset:
        return AsyncDataset(self._client, self._function.dataset_uuid)


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

    async def call(
        self,
        name: str = None,
        instructions: str = "you are a helpful assistant",
        input_type: Optional[Any] = None,
        input: Any = str,
        output_type: Optional[type[T]] = None,
        model: Optional[str] = None,
        examples: Optional[List[Example]] = None,
        configuration: Optional[CallConfiguration] = None,
    ) -> Tuple[T, AsyncFunctionResponse]:
        """Calls a function
        Arguments:
            name: str: the name of the function, if not provided, it will be generated from the instructions
            instructions: str: the instructions for the function
            input_type: Any: the input type for the function
            input: Any: the input to the function
            output_type: Any: the output type for the function
                There is one special output type:
                    - `ImageOutput`: the output will be an image
            model: str: the model to use for the function
            examples: List[Example]: A list of examples to help guide the function's response

        Returns:
            tuple[Any, FunctionResponse]: the output of the function and the response object. The type of the output is determined by the output_type. If the output_type is a `Pydantic` model, the output will be validated against the schema.
        """
        if (
            output_type
            and isinstance(output_type, type)
            and issubclass(output_type, ImageOutput)
        ):
            res = await self._client.generate_image(prompt=input)
            return res

        if not name:
            name = djb2(instructions)

        input_schema = type_to_json_schema(input_type)
        output_schema = type_to_json_schema(output_type)

        input = prepare_input(input)

        _examples = []
        if examples:
            for example in examples:
                input = prepare_input(example.input)
                output = prepare_input(example.output)
                _examples.append(Example(input=str(input), output=str(output)))

        call_payload = CallPayload(
            name=name,
            instructions=instructions,
            input_type=input_schema,
            input=input,
            output_type=output_schema,
            model=model,
            examples=_examples,
        )

        res: FunctionResponseModel = await self._client.call(call_payload)

        if output_type is not None:
            if inspect.isclass(output_type) and issubclass(output_type, BaseModel):
                return output_type.model_validate(
                    res.json_payload
                ), AsyncFunctionResponse(client=self._client, **res.model_dump())
            elif (
                (get_origin(output_type) == list or get_origin(output_type) is List)
                and inspect.isclass(get_args(output_type)[0])
                and issubclass(get_args(output_type)[0], BaseModel)
            ):
                return [
                    get_args(output_type)[0].model_validate(item)
                    for item in res.json_payload
                ], AsyncFunctionResponse(client=self._client, **res.model_dump())
            else:
                return res.json_payload, AsyncFunctionResponse(
                    client=self._client, **res.model_dump()
                )

        return res.message, AsyncFunctionResponse(
            client=self._client, **res.model_dump()
        )
