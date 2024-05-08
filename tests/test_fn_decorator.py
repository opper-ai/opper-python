from typing import Dict, List, Optional, Union
from unittest.mock import MagicMock, patch

import pytest
from jsonschema import validate
from opperai import AsyncClient, Client, fn
from opperai.core.utils import convert_function_call_to_json
from opperai.functions.decorator._schemas import type_to_json_schema
from pydantic import BaseModel


def test_fn_decorator(client: Client, vcr_cassette):
    @fn(client=client)
    def translate(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    translation = translate("Hello", "es")
    assert translation == "Hola"

    translation, response = translate.call("Hello", "es")
    assert translation == "Hola"

    response.span.save_metric("metric", 1)


@pytest.mark.asyncio(scope="module")
async def test_fn_decorator_async(aclient: AsyncClient, vcr_cassette):
    @fn(client=aclient)
    async def translate(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    translation = await translate("Hello", "es")
    assert translation == "Hola"

    translation, response = await translate.call("Hello", "es")
    assert translation == "Hola"

    await response.span.save_metric("metric", 1)


@patch("opperai.core._http_clients._http_client.do_request")
def test_decorator(mock_do_request):
    mock_do_request.side_effect = [
        MagicMock(status_code=404),
        MagicMock(
            status_code=200,
            json=lambda: {
                "id": 1,
                "path": "path",
                "description": "description",
                "instructions": "instructions",
            },
        ),
        MagicMock(status_code=200, json=lambda: {"json_payload": "Hola"}),
        MagicMock(status_code=404),
        MagicMock(
            status_code=200,
            json=lambda: {
                "id": 2,
                "path": "path",
                "description": "description",
                "instructions": "instructions",
            },
        ),
        MagicMock(status_code=200, json=lambda: {"json_payload": ["Hola", "Bonjour"]}),
    ]

    @fn()
    def translate(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    @fn()
    def translate_list(text: str, target_languages: List[str]) -> List[str]:
        """Translate text to a list of target languages."""

    assert translate("Hello", "es") == "Hola"
    assert translate_list("Hello", ["es", "fr"]) == ["Hola", "Bonjour"]


@patch("opperai.core._http_clients._http_client.do_request")
def test_decorator_supply_model(mock_do_request):
    mock_do_request.side_effect = [
        MagicMock(status_code=404),
        MagicMock(
            status_code=200,
            json=lambda: {
                "id": 1,
                "path": "path",
                "description": "description",
                "instructions": "instructions",
            },
        ),
        MagicMock(status_code=200, json=lambda: {"json_payload": "Hola"}),
        MagicMock(status_code=404),
        MagicMock(
            status_code=200,
            json=lambda: {
                "id": 2,
                "path": "path",
                "description": "description",
                "instructions": "instructions",
            },
        ),
        MagicMock(status_code=200, json=lambda: {"json_payload": ["Hola", "Bonjour"]}),
    ]

    @fn(model="gpt-4-0125-preview")
    def translate(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    @fn()
    def translate_list(text: str, target_languages: List[str]) -> List[str]:
        """Translate text to a list of target languages."""

    assert translate("Hello", "es") == "Hola"
    assert translate_list("Hello", ["es", "fr"]) == ["Hola", "Bonjour"]


class NestedModel(BaseModel):
    nested_integer: int
    nested_string: str


class ExampleModel(BaseModel):
    integer_field: int
    float_field: float
    string_field: str
    boolean_field: bool
    optional_field: Optional[int]
    list_field: List[int]
    union_field: Union[int, str]
    dict_field: Dict[str, int]
    nested_model: NestedModel
    list_of_models: List[NestedModel]


def test_convert_func_to_json():
    def something(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    json = convert_function_call_to_json(something, "Hello", "es")
    assert json == {"text": "Hello", "target_language": "es"}

    model = ExampleModel(
        integer_field=1,
        float_field=1.0,
        string_field="string",
        boolean_field=True,
        optional_field=1,
        list_field=[1, 2, 3],
        union_field="string",
        dict_field={"key": 1},
        nested_model=NestedModel(nested_integer=1, nested_string="string"),
        list_of_models=[
            NestedModel(nested_integer=1, nested_string="string"),
            NestedModel(nested_integer=1, nested_string="string"),
        ],
    )

    def advanced(text: str, target_language: str, model: ExampleModel) -> str:
        pass

    json = convert_function_call_to_json(advanced, "Hello", "es", model)
    assert json == {
        "text": "Hello",
        "target_language": "es",
        "model": model.model_dump(),
    }


class ToyModel(BaseModel):
    name: str


class ChildModel(BaseModel):
    toy: ToyModel
    toys: List[ToyModel]


class ParentModel(BaseModel):
    child: ChildModel
    children: List[ChildModel]


@pytest.mark.parametrize(
    "type_input,  example_input",
    [
        (int, 1),
        (str, "string"),
        (float, 1.0),
        (bool, True),
        # (Dict[str, int], {"key": 1}),
        (List[int], [1, 2, 3]),
        (
            ParentModel,
            {
                "child": {
                    "toy": {"name": "name"},
                    "toys": [{"name": "name"}],
                },
                "children": [{"toy": {"name": "name"}, "toys": [{"name": "name"}]}],
            },
        ),
        (
            List[ParentModel],
            [
                {
                    "child": {
                        "toy": {"name": "name"},
                        "toys": [{"name": "name"}],
                    },
                    "children": [{"toy": {"name": "name"}, "toys": [{"name": "name"}]}],
                }
            ],
        ),
        (
            List[List[ParentModel]],
            [
                [
                    {
                        "child": {
                            "toy": {"name": "name"},
                            "toys": [{"name": "name"}],
                        },
                        "children": [
                            {"toy": {"name": "name"}, "toys": [{"name": "name"}]}
                        ],
                    }
                ],
            ],
        ),
    ],
)
def test_type_to_json_schema(type_input, example_input):
    schema = type_to_json_schema(type_input)
    print(schema)
    assert validate(example_input, schema) is None
