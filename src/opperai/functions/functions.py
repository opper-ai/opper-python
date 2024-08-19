import itertools
import json
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Tuple, TypeVar, Union

from opperai._client import Client
from opperai.datasets.datasets import Dataset
from opperai.functions.decorator._schemas import type_to_json_schema
from opperai.types import (
    ChatPayload,
    Example,
    ImageMessageContent,
    Message,
    StreamingChunk,
)
from opperai.types import Function as FunctionModel
from opperai.types import FunctionResponse as FunctionResponseModel
from pydantic import BaseModel, PrivateAttr

from ..spans.spans import Span

T = TypeVar("T", bound=Any)


class FunctionResponse(FunctionResponseModel):
    _client: Client = PrivateAttr()

    def __init__(self, client: Client = None, **kwargs):
        super().__init__(**kwargs)
        if not client:
            client = Client()
        self._client = client

    @property
    def span(self):
        return Span(self._client, self.span_id)


class StreamingResponse:
    _client: Client = None
    _head: StreamingChunk = None
    _stream: Iterator[StreamingChunk] = None
    context: List[Dict[str, Any]] = []
    span: Span = None

    def __init__(
        self,
        client: Client = None,
        stream: Iterator[StreamingChunk] = None,
    ):
        if not client:
            client = Client()
        self._client = client

        _stream, _head = itertools.tee(stream)
        self._stream = _stream

        head = next(_head)
        self.span = Span(self._client, head.span_id)
        self.context = head.context if head.context else []

    @property
    def deltas(self) -> Iterator[str]:
        for chunk in self._stream:
            if chunk.delta is not None:
                yield chunk.delta


@dataclass
class Function:
    _client: Client
    _function: FunctionModel

    def chat(
        self,
        messages: List[Message],
        parent_span_id: Optional[str] = None,
        stream: Optional[bool] = False,
    ) -> Union[FunctionResponse, StreamingResponse]:
        if stream:
            if self._function.out_schema is not None:
                raise ValueError(
                    "Cannot stream output for functions structured response"
                )

            response: Iterator[StreamingChunk] = self._client.functions.chat(
                function_path=self._function.path,
                data=ChatPayload(messages=messages, parent_span_uuid=parent_span_id),
                stream=stream,
            )

            return StreamingResponse(client=self._client, stream=response)

        response: FunctionResponseModel = self._client.functions.chat(
            function_path=self._function.path,
            data=ChatPayload(messages=messages, parent_span_uuid=parent_span_id),
            stream=stream,
        )

        return FunctionResponse(client=self._client, **response.model_dump())

    def dataset(self) -> Dataset:
        return Dataset(self._client, self._function.dataset_uuid)

    def delete(self) -> bool:
        return self._client.functions.delete(uuid=self._function.uuid)

    def flush_cache(self) -> bool:
        return self._client.functions.flush_cache(uuid=self._function.uuid)

    def update(self, **kwargs) -> "Function":
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
        updated_function = self._client.functions.update(
            uuid=self._function.uuid, function=updated_model
        )
        self._function = updated_function

        return self


@dataclass
class Functions:
    _client: Client = None

    def __init__(self, client: Client = None):
        if client is None:
            client = Client()

        self._client = client

    def create(
        self,
        path: str,
        instructions: str,
        description: Optional[str] = None,
        input_type: Optional[Any] = None,
        output_type: Optional[Any] = None,
        model: Optional[str] = None,
    ) -> Function:
        try:
            function = self.get(path=path)
            if function:
                return function.update(
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

        function = self._client.functions.create(
            FunctionModel(
                path=path,
                instructions=instructions,
                description=description,
                input_schema=input_schema if input_type else None,
                out_schema=output_schema if output_type else None,
                model=model,
            )
        )

        return Function(self._client, function)

    def get(self, uuid: str = None, path: str = None) -> Optional[Function]:
        if uuid is not None:
            function = self._client.functions.get(uuid=uuid)
        elif path is not None:
            function = self._client.functions.get(path=path)
        else:
            raise ValueError("Either uuid or path must be provided")

        if not function:
            return None

        return Function(self._client, function)

    def delete(self, uuid: str = None, path: str = None) -> bool:
        if uuid is not None:
            return self._client.functions.delete(uuid=uuid)
        elif path is not None:
            return self._client.functions.delete(path=path)
        else:
            raise ValueError("Either uuid or path must be provided")

    def call(
        self,
        name: str = None,
        instructions: str = "you are a helpful assistant",
        input_type: Optional[Any] = None,
        input: Any = str,
        output_type: Optional[type[T]] = None,
        model: Optional[str] = None,
        examples: Optional[List[Example]] = None,
    ) -> Tuple[T, FunctionResponse]:
        """Calls a function
        Arguments:
            name: str: the name of the function, if not provided, it will be generated from the instructions
            instructions: str: the instructions for the function
            input_type: Any: the input type for the function
            input: Any: the input to the function
            output_type: Any: the output type for the function
            model: str: the model to use for the function
            examples: List[Example]: A list of examples to help guide the function's response.

        Returns:
            tuple[Any, FunctionResponse]: the output of the function and the response object. The type of the output is determined by the output_type. If the output_type is a `Pydantic` model, the output will be validated against the schema.
        """
        if not name:
            name = djb2(instructions)

        input_schema = type_to_json_schema(input_type)
        output_schema = type_to_json_schema(output_type)

        function = FunctionModel(
            path=name,
            instructions=instructions,
            input_schema=input_schema,
            out_schema=output_schema,
            model=model,
        )
        self._client.functions.create(function)

        input, images = prepare_input(input)

        messages = [Message(role="user", content=json.dumps(input))]
        if images:
            messages.append(Message(role="user", content=images))

        _examples = []
        if examples:
            for example in examples:
                input, _ = prepare_input(example.input)
                output, _ = prepare_input(example.output)
                _examples.append(Example(input=str(input), output=str(output)))

        res: FunctionResponseModel = self._client.functions.chat(
            function_path=name, data=ChatPayload(messages=messages), examples=_examples
        )

        if output_type is not None:
            if issubclass(output_type, BaseModel):
                return output_type.model_validate(res.json_payload), FunctionResponse(
                    client=self._client, **res.model_dump()
                )
            else:
                return res.json_payload, FunctionResponse(
                    client=self._client, **res.model_dump()
                )

        return res.message, FunctionResponse(client=self._client, **res.model_dump())


def prepare_input(input: Any) -> Tuple[List[str], List[ImageMessageContent]]:
    def _prepare_input(
        input: Any, _input: List[str] = [], images: List[ImageMessageContent] = []
    ):
        if isinstance(input, ImageMessageContent):
            return None, input
        if isinstance(input, BaseModel):
            return input.model_dump(), None
        if isinstance(input, list):
            inputs = []
            images = []
            for item in input:
                _input, _image = _prepare_input(item)
                if _input:
                    inputs.append(_input)
                if _image:
                    images.append(_image)
            return inputs, images
        if isinstance(input, dict):
            inputs = {}
            for k, v in input.items():
                _input, _image = _prepare_input(v)
                if _input:
                    inputs[k] = _input
                if _image:
                    images.append(_image)
            return inputs, images
        return input, None

    return _prepare_input(input)


def djb2(s: str):
    bytes = s.encode("utf-8")
    hash = 5381
    for x in bytes:
        hash = ((hash << 5) + hash) + x
    return str(abs(hash))
