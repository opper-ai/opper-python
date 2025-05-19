import os
from pathlib import Path

import pytest

from opperai.types import ImageInput, validate_uuid_xor_path


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


def test_image_input_mime_detection():
    # Test PNG detection
    png_path = Path("tests/fixtures/images/minimal.png")
    png_input = ImageInput(path=png_path)
    png_result = png_input._opper_image_input
    assert "data:image/png;base64," in png_result

    # Test JPEG detection
    jpg_path = Path("tests/fixtures/images/fossil.jpg")
    jpg_input = ImageInput(path=jpg_path)
    jpg_result = jpg_input._opper_image_input
    assert "data:image/jpeg;base64," in jpg_result

    # Test invalid path
    with pytest.raises(ValueError, match="no path provided"):
        invalid_input = ImageInput()
        invalid_input._opper_image_input

    # Test unsupported file type (create a temporary text file)
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp.write(b"This is a text file, not an image")
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="File type not supported"):
            text_input = ImageInput(path=Path(tmp_path))
            text_input._opper_image_input
    finally:
        os.unlink(tmp_path)  # Clean up the temporary file
