from dataclasses import dataclass
from typing import Any, List, Optional

from pydantic import PrivateAttr

from opperai._client import Client
from opperai.core.functions.decorator._schemas import type_to_json_schema
from opperai.types import ChatPayload, Message
from opperai.types import Function as FunctionModel
from opperai.types import FunctionResponse as FunctionResponseModel

from .spans import Span


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


@dataclass
class Function:
    _client: Client
    _function: FunctionModel

    def chat(
        self, messages: List[Message], parent_span_id: Optional[str] = None
    ) -> FunctionResponse:
        response = self._client.functions.chat(
            function_path=self._function.path,
            data=ChatPayload(messages=messages, parent_span_uuid=parent_span_id),
        )
        return FunctionResponse(client=self._client, **response.model_dump())

    def delete(self) -> bool:
        return self._client.functions.delete(id=self._function.id)

    def flush_cache(self) -> bool:
        return self._client.functions.flush_cache(id=self._function.id)

    def update(self, **kwargs) -> "Function":
        updated = self._function.model_dump(exclude_none=True)
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
            id=self._function.id, function=updated_model
        )
        self._function = updated_function

        return self


@dataclass
class Functions:
    _client: Client = Client()

    def create(
        self,
        path: str,
        description: Optional[str] = None,
        input_type: Optional[Any] = None,
        output_type: Optional[Any] = None,
        instructions: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Function:
        try:
            function = self.get(path=path)
            if function:
                return function.update(
                    description=description,
                    input_type=input_type,
                    output_type=output_type,
                    instructions=instructions,
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
                description=description,
                input_schema=input_schema if input_type else None,
                out_schema=output_schema if output_type else None,
                instructions=instructions,
                model=model,
            )
        )

        return Function(self._client, function)

    def get(self, id: int = None, path: str = None) -> Optional[Function]:
        if id is not None:
            function = self._client.functions.get(id=id)
        elif path is not None:
            function = self._client.functions.get(path=path)
        else:
            raise ValueError("Either id or name must be provided")

        if not function:
            return None

        return Function(self._client, function)

    def delete(self, id: int = None, path: str = None) -> bool:
        if id is not None:
            return self._client.functions.delete(id=id)
        elif path is not None:
            return self._client.functions.delete(path=path)
        else:
            raise ValueError("Either id or name must be provided")
