from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from opperai.core.utils import prepare_input


class TestUtils:
    class TestPrepareInput:
        def test_prepare_input(self):
            # test basic functionality with various types
            assert prepare_input("hello") == "hello"
            assert prepare_input(42) == 42
            assert prepare_input(True) is True

        def test_prepare_input_with_datetime(self):
            dt = datetime(2023, 1, 1, 12, 0, 0)
            result = prepare_input(dt)
            assert result == "2023-01-01T12:00:00"

        def test_prepare_input_with_pydantic_model(self):
            class TestModel(BaseModel):
                name: str
                age: int
                email: Optional[str] = None
                date: datetime

            dt = datetime(2023, 1, 1, 12, 0, 0)
            model = TestModel(name="john", age=30, date=dt)
            result = prepare_input(model)
            expected = {
                "name": "john",
                "age": 30,
                "date": "2023-01-01T12:00:00",
            }
            assert result == expected

        def test_prepare_input_with_list(self):
            dt = datetime(2023, 1, 1, 12, 0, 0)
            input_list = ["hello", 42, dt, True]
            result = prepare_input(input_list)
            expected = ["hello", 42, "2023-01-01T12:00:00", True]
            assert result == expected

        def test_prepare_input_with_dict(self):
            dt = datetime(2023, 1, 1, 12, 0, 0)
            input_dict = {"text": "hello", "number": 42, "date": dt, "flag": True}
            result = prepare_input(input_dict)
            expected = {
                "text": "hello",
                "number": 42,
                "date": "2023-01-01T12:00:00",
                "flag": True,
            }
            assert result == expected

        def test_prepare_input_with_none(self):
            result = prepare_input(None)
            assert result is None

        def test_prepare_input_with_int(self):
            result = prepare_input(42)
            assert result == 42

        def test_prepare_input_with_float(self):
            result = prepare_input(3.14)
            assert result == 3.14

        def test_prepare_input_with_bool(self):
            result = prepare_input(True)
            assert result is True
            result = prepare_input(False)
            assert result is False

        def test_prepare_input_with_str(self):
            result = prepare_input("hello world")
            assert result == "hello world"
