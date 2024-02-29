import os
import uuid
from unittest.mock import MagicMock, patch

from opperai import fn, trace

os.environ["OPPER_API_KEY"] = "api-key"


@patch("opperai._http_clients._http_client.do_request")
def test_decorator(mock_do_request):
    mock_do_request.side_effect = [
        MagicMock(status_code=200, json=lambda: {"uuid": str(uuid.uuid4())}),
        MagicMock(status_code=200, json=lambda: {"uuid": str(uuid.uuid4())}),
    ]

    @trace
    def something(text: str, target_language: str) -> str:
        return "Hola"

    assert something("Hello", "es") == "Hola"
