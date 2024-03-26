import os
import uuid
from unittest.mock import MagicMock, patch
from datetime import datetime

from uuid import uuid4
from opperai.types.spans import Span
from opperai import Client

from opperai import trace


@patch("opperai._http_clients._http_client.do_request")
def test_decorator(mock_do_request):
    mock_do_request.side_effect = [
        MagicMock(status_code=200, json=lambda: {"uuid": str(uuid.uuid4())}),
        MagicMock(status_code=200, json=lambda: {"uuid": str(uuid.uuid4())}),
    ]

    @trace(client=Client(api_key="temporary", api_url="temporary"))
    def something(text: str, target_language: str) -> str:
        return "Hola"

    assert something("Hello", "es") == "Hola"
