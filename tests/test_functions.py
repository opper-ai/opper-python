import pytest
from opperai import AsyncClient, Client
from opperai.types import ChatPayload, Message

from unittest.mock import patch

api_key = "key"


@patch("opperai.client._http_client.do_request")
def test_chat(mock_do_request):
    mock_do_request.return_value = {"message": "Bonjour"}
    client = Client(api_key=api_key)
    resp = client.functions.chat(
        "french", ChatPayload(messages=[Message(role="user", content="hello")])
    )

    assert resp.message == "Bonjour"
    mock_do_request.assert_called_once()


@pytest.mark.asyncio
@patch("opperai.client._async_http_client.do_request")
async def test_async_chat(mock_do_request):
    mock_do_request.return_value = {"message": "Bonjour"}
    client = AsyncClient(api_key="op-dev-api-key", api_url="http://localhost:8000")
    resp = await client.functions.chat(
        "french", ChatPayload(messages=[Message(role="user", content="hello")])
    )

    assert resp.message == "Bonjour"
    mock_do_request.assert_called_once()
