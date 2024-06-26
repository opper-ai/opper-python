import pytest
from opperai.types import validate_uuid_xor_path


def test_id_xor_path():
    @validate_uuid_xor_path
    def test_function(uuid=None, path=None):
        return uuid, path

    assert test_function(uuid=1) == (1, None)

    assert test_function(path="test") == (None, "test")

    with pytest.raises(ValueError):
        test_function(uuid=1, path="test")

    with pytest.raises(ValueError):
        test_function()

    with pytest.raises(ValueError):
        test_function(uuid=1, path="test", other="other")
