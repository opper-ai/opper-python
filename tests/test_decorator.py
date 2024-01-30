import os
from typing import Dict, List, Optional, Union

from opperai import fn
from opperai.functions.decorator._schemas import (
    convert_function_call_to_json,
)
from pydantic import BaseModel

os.environ["OPPER_API_KEY"] = "op-dev-api-key"
os.environ["OPPER_API_URL"] = "http://localhost:8000"


@fn()
def translate(text: str, target_language: str) -> str:
    """Translate text to a target language."""


@fn()
def translate_list(text: str, target_languages: List[str]) -> List[str]:
    """Translate text to a list of target languages."""


def test_decorator():
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
