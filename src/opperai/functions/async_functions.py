import inspect
import sys
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    get_args,
    get_origin,
    overload,
)

from opperai._client import AsyncClient
from opperai.core.spans import get_current_span_id
from opperai.datasets.async_datasets import AsyncDataset
from opperai.functions.decorator._schemas import type_to_json_schema
from opperai.types import (
    CacheConfiguration,
    CallConfiguration,
    CallPayload,
    ChatPayload,
    Example,
    FunctionConfiguration,
    ImageOutput,
    Message,
    StreamingChunk,
)
from opperai.types import Function as FunctionModel
from opperai.types import FunctionResponse as FunctionResponseModel
from pydantic import BaseModel, PrivateAttr

from ..spans.async_spans import AsyncSpan
from .functions import T, prepare_examples, prepare_input

if sys.version_info < (3, 10):

    async def anext(iterator):
        try:
            return await iterator.__anext__()
        except StopAsyncIteration:
            raise StopAsyncIteration


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
    stream: Optional[Iterator[StreamingChunk]] = None
    _context: Optional[List[Dict[str, Any]]] = None
    _span_id: Optional[str] = None

    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        stream: Optional[Iterator[StreamingChunk]] = None,
    ):
        if not client:
            client = AsyncClient()
        self._client = client
        self.stream = stream

    async def initialize(self):
        try:
            first_chunk = await anext(self.stream)
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

            response = await self._client.functions.chat(
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

    @overload
    async def call(
        self,
        input: Any = None,
        output_type: Optional[Any] = None,
        examples: Optional[List[Example]] = None,
        configuration: Optional[CallConfiguration] = None,
        stream: Literal[True] = True,
    ) -> AsyncStreamingResponse: ...

    @overload
    async def call(
        self,
        input: Any = None,
        output_type: Optional[Any] = None,
        examples: Optional[List[Example]] = None,
        configuration: Optional[CallConfiguration] = None,
        stream: Literal[False] = False,
    ) -> Tuple[T, AsyncFunctionResponse]: ...

    async def call(
        self,
        input: Any = None,
        output_type: Optional[Any] = None,
        examples: Optional[List[Example]] = None,
        configuration: Optional[CallConfiguration] = None,
        stream: Optional[bool] = False,
    ) -> Tuple[T, AsyncFunctionResponse]:
        """
        Calls a function with the given input and optional output type.

        If the output type is provided, the response will be cast to the output type.
        If the output type is not provided, the response will be returned as json.
        """
        payload = CallPayload(
            input=input,
            examples=examples,
            stream=stream,
        )
        if configuration:
            payload.configuration = configuration

        res = await self._client.functions.call(
            uuid=self._function.uuid,
            payload=payload,
        )
        if stream:
            res = AsyncStreamingResponse(client=self._client, stream=res)
            await res.initialize()
            return res

        # if output_type is provided attempt to cast the response to the output type
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

        result = res.json_payload if res.json_payload is not None else res.message

        return result, AsyncFunctionResponse(client=self._client, **res.model_dump())

    async def delete(self) -> bool:
        return await self._client.functions.delete(uuid=self._function.uuid)

    async def flush_cache(self) -> bool:
        return await self._client.functions.flush_cache(uuid=self._function.uuid)

    async def update(self, **kwargs) -> "AsyncFunction":
        updated = self._function.model_dump(exclude_none=True)

        if "input_type" in kwargs:
            kwargs["input_schema"] = type_to_json_schema(kwargs["input_type"])
            del kwargs["input_type"]

        if "output_type" in kwargs:
            kwargs["out_schema"] = type_to_json_schema(kwargs["output_type"])
            del kwargs["output_type"]

        if "configuration" in kwargs and kwargs["configuration"] is not None:
            cfg: FunctionConfiguration = kwargs["configuration"]
            kwargs["cache_configuration"] = CacheConfiguration(
                exact_match_cache_ttl=cfg.cache.exact_match_cache_ttl,
                semantic_cache_threshold=cfg.cache.semantic_cache_threshold,
                semantic_cache_ttl=cfg.cache.semantic_cache_ttl,
            )
            del kwargs["configuration"]

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

    def __init__(self, client: Optional[AsyncClient] = None):
        if client is None:
            client = AsyncClient()

        self._client = client

    async def create(
        self,
        name: str,
        instructions: str,
        description: Optional[str] = None,
        input_type: Optional[Any] = None,
        output_type: Optional[Any] = None,
        model: Optional[str] = None,
        configuration: Optional[FunctionConfiguration] = None,
    ) -> AsyncFunction:
        try:
            function = await self.get(name=name)
            if function:
                return await function.update(
                    instructions=instructions,
                    description=description,
                    input_type=input_type,
                    output_type=output_type,
                    model=model,
                    configuration=configuration,
                )
        except Exception:
            pass

        if input_type:
            input_schema = type_to_json_schema(input_type)
        if output_type:
            output_schema = type_to_json_schema(output_type)

        function = await self._client.functions.create(
            FunctionModel(
                path=name,
                instructions=instructions,
                description=description,
                input_schema=input_schema if input_type else None,
                out_schema=output_schema if output_type else None,
                model=model,
                cache_configuration=configuration.cache if configuration else None,
            )
        )

        return AsyncFunction(self._client, function)

    async def get(
        self,
        uuid: Optional[str] = None,
        path: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Optional[AsyncFunction]:
        if uuid is not None:
            function = await self._client.functions.get(uuid=uuid)
        elif path is not None:
            function = await self._client.functions.get(path=path)
        elif name is not None:
            function = await self._client.functions.get(path=name)
        else:
            raise ValueError("Either id or name must be provided")

        if not function:
            return None

        return AsyncFunction(self._client, function)

    async def delete(
        self,
        uuid: Optional[str] = None,
        path: Optional[str] = None,
        name: Optional[str] = None,
    ) -> bool:
        if uuid is not None:
            return await self._client.functions.delete(uuid=uuid)
        elif path is not None:
            return await self._client.functions.delete(path=path)
        elif name is not None:
            return await self._client.functions.delete(path=name)
        else:
            raise ValueError("Either id or name must be provided")

    @overload
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
        parent_span_id: Optional[str] = None,
        stream: Literal[True] = True,
        fallback_models: Optional[List[str]] = None,
    ) -> AsyncStreamingResponse: ...

    @overload
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
        parent_span_id: Optional[str] = None,
        stream: Literal[False] = False,
        fallback_models: Optional[List[str]] = None,
    ) -> Tuple[T, AsyncFunctionResponse]: ...

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
        parent_span_id: Optional[str] = None,
        stream: Optional[bool] = False,
        fallback_models: Optional[List[str]] = None,
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
            stream: bool: whether to stream the response

        Returns:
            tuple[Any, FunctionResponse]: the output of the function and the response object. The type of the output is determined by the output_type. If the output_type is a `Pydantic` model, the output will be validated against the schema.
        """
        if (
            output_type
            and isinstance(output_type, type)
            and issubclass(output_type, ImageOutput)
        ):
            res = await self._client.generate_image(
                prompt=input, model=model, configuration=configuration
            )
            return res

        input_schema = type_to_json_schema(input_type)
        output_schema = type_to_json_schema(output_type)

        _input = prepare_input(input)
        _examples = prepare_examples(examples)

        call_payload = CallPayload(
            name=name,
            instructions=instructions,
            input_schema=input_schema,
            input=_input,
            output_schema=output_schema,
            model=model,
            examples=_examples,
            parent_span_uuid=parent_span_id
            if parent_span_id
            else get_current_span_id(),
            stream=stream,
            fallback_models=fallback_models,
        )
        if configuration:
            call_payload.configuration = configuration

        res = await self._client.call(call_payload)
        if stream:
            res = AsyncStreamingResponse(client=self._client, stream=res)
            await res.initialize()
            return res

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
