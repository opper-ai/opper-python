from typing import Dict, List, Optional, Union

import pytest
from jsonschema import validate
from opperai import AsyncClient, Client, fn
from opperai.core.utils import convert_function_call_to_json
from opperai.functions.decorator._schemas import type_to_json_schema
from opperai.types import ImageInput
from pydantic import BaseModel


def test_fn_decorator_on_method(client: Client, vcr_cassette):
    class TestClass(BaseModel):
        data: str

        @fn(client=client)
        def test_method(self, text: str) -> str:
            """say hello"""

    test = TestClass(data="Hello")

    res = test.test_method()
    assert "hello" in res.lower()

    res, _ = test.test_method.call("Hello")
    assert "hello" in res.lower()


@pytest.mark.asyncio(scope="module")
async def test_fn_decorator_on_method_async(aclient: AsyncClient, vcr_cassette):
    class TestClass(BaseModel):
        data: str

        @fn(client=aclient)
        async def test_method(self, text: str) -> str:
            """say hello"""

    test = TestClass(data="Hello")

    res = await test.test_method()
    assert "hello" in res.lower()

    res, _ = await test.test_method.call("Hello")
    assert "hello" in res.lower()


def test_fn_decorator_image(client: Client, vcr_cassette):
    class ImageDescription(BaseModel):
        description: str

    @fn(client=client, model="openai/gpt-4o")
    def describe_image(
        image: ImageInput,
    ) -> ImageDescription:
        """given an image describe what it is"""

    description = describe_image(
        ImageInput.from_path("tests/fixtures/images/fossil.png"),
    )
    print(description)

    assert "fossil" in description.description.lower()


@pytest.mark.asyncio(scope="module")
async def test_fn_decorator_image_async(aclient: AsyncClient, vcr_cassette):
    class Word(BaseModel):
        letters: List[str]

    @fn(client=aclient, model="openai/gpt-4o")
    async def extract_letters(
        image: ImageInput,
    ) -> Word:
        """given an image extract the word it represents"""

    word = await extract_letters(
        ImageInput.from_path("tests/fixtures/images/letters.png"),
    )
    print(word)

    assert [x.lower() for x in word.letters] == ["l", "e", "t", "t", "e", "r"]


def hola_in_word(word: str):
    return "hola" in word.lower()


def test_fn_decorator(client: Client, vcr_cassette):
    @fn(client=client)
    def translate(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    translation = translate("Hello", "es")
    assert hola_in_word(translation)

    translation, response = translate.call("Hello", "es")
    assert hola_in_word(translation)

    response.span.save_metric("metric", 1)


import os

os.environ["OPPER_API_KEY"] = "op-FNHF7LJGR12KE00BBQH0"
os.environ["OPPER_API_URL"] = "http://localhost:8000"


@pytest.mark.asyncio
async def test_fn_decorator_async(aclient: AsyncClient, vcr_cassette):
    @fn(client=aclient)
    async def translate(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    translation = await translate("Hello", "es")
    assert hola_in_word(translation)

    translation, response = await translate.call("Hello", "es")
    assert hola_in_word(translation)

    await response.span.save_metric("metric", 1)


def test_decorator(client: Client, vcr_cassette):
    @fn(client=client)
    def translate(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    @fn(client=client)
    def translate_list(text: str, target_languages: List[str]) -> List[str]:
        """Translate text to a list of target languages."""

    assert translate("Hello", "es") == "Hola"
    assert translate_list("Hello", ["es", "fr"]) == ["Hola", "Bonjour"]


@pytest.mark.asyncio
async def test_decorator_supply_model(aclient: AsyncClient, vcr_cassette):
    @fn(client=aclient, model="openai/gpt-4o")
    async def translate(text: str, target_language: str) -> str:
        """Translate text to a target language."""

    @fn(client=aclient, model="openai/gpt-4o")
    async def translate_list(text: str, target_languages: List[str]) -> List[str]:
        """Translate text to a list of target languages."""

    assert await translate("Hello", "es") == "Hola"
    assert await translate_list("Hello", ["es", "fr"]) == ["Hola", "Bonjour"]


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

    input = convert_function_call_to_json(something, "Hello", "es")
    assert input == {"text": "Hello", "target_language": "es"}

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

    input = convert_function_call_to_json(advanced, "Hello", "es", model)
    assert input == {
        "text": "Hello",
        "target_language": "es",
        "model": model.model_dump(),
    }


def test_convert_func_to_json_with_image():
    def f(image: ImageInput, text: str) -> str:
        pass

    input = convert_function_call_to_json(
        f, ImageInput.from_path("tests/fixtures/images/minimal.png"), "Hello"
    )
    assert input == {
        "image": {
            "_opper_image_input": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQAAAAA3bvkkAAAACklEQVR4AWNgAAAAAgABc3UBGAAAAABJRU5ErkJggg=="
        },
        "text": "Hello",
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
