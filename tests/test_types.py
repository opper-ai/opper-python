import pytest
from opperai.types import validate_id_xor_path


def test_id_xor_path():
    @validate_id_xor_path
    def test_function(id=None, path=None):
        return id, path

    assert test_function(id=1) == (1, None)

    assert test_function(path="test") == (None, "test")

    with pytest.raises(ValueError):
        test_function(id=1, path="test")

    with pytest.raises(ValueError):
        test_function()

    with pytest.raises(ValueError):
        test_function(id=1, path="test", other="other")
