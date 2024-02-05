from unittest.mock import MagicMock, patch

import pytest
from opperai import AsyncClient, Client
from opperai.types import ChatPayload, FunctionDescription, Message

api_key = "key"


@patch("opperai._http_clients._http_client.do_request")
def test_chat(mock_do_request):
    mock_do_request.return_value = MagicMock(
        status_code=200, json=lambda: {"message": "Bonjour"}
    )
    client = Client(api_key=api_key)
    resp = client.functions.chat(
        "french", ChatPayload(messages=[Message(role="user", content="hello")])
    )

    assert resp.message == "Bonjour"
    mock_do_request.assert_called_once()


@pytest.mark.asyncio
@patch("opperai._http_clients._http_client.stream")
async def test_chat_stream(mock_stream):
    def gen():
        yield {"delta": "Bon"}
        yield {"delta": "Jour"}

    mock_stream.return_value = gen()
    client = Client(api_key="op-dev-api-key", api_url="http://localhost:8000")
    gen = client.functions.chat(
        "french",
        ChatPayload(messages=[Message(role="user", content="hello")]),
        stream=True,
    )
    resp = ""
    for message in gen:
        resp += message.delta

    assert resp == "BonJour"


@pytest.mark.asyncio
@patch("opperai._http_clients._http_client.do_request")
async def test_create_function(mock_do_request):
    mock_do_request.side_effect = [
        MagicMock(
            status_code=404,
        ),  # Response for get_function_by_path
        MagicMock(
            status_code=200, json=lambda: {"id": 1}
        ),  # Response for create_function
    ]
    client = Client(api_key="op-dev-api-key", api_url="http://localhost:8000")
    function = FunctionDescription(
        path="test/path", description="Test function", instructions="Do something"
    )
    function_id = client.functions.create_function(function)
    assert function_id == 1
    assert mock_do_request.call_count == 2
    mock_do_request.assert_any_call(
        "GET",
        "/api/v1/functions/by_path/test/path",
    )
    mock_do_request.assert_any_call(
        "POST",
        "/api/v1/functions",
        json=function.model_dump(),
    )


@pytest.mark.asyncio
@patch("opperai._http_clients._http_client.do_request")
async def test_update_function(mock_do_request):
    mock_do_request.return_value = MagicMock(status_code=200, json=lambda: {"id": 1})
    client = Client(api_key="op-dev-api-key", api_url="http://localhost:8000")
    function = FunctionDescription(
        id=1,
        path="test/path",
        description="Updated Test function",
        instructions="Do something else",
    )
    function_id = client.functions.update_function(function)
    assert function_id == 1
    mock_do_request.assert_called_once()


@pytest.mark.asyncio
@patch("opperai._http_clients._http_client.do_request")
async def test_get_function_by_path(mock_do_request):
    mock_do_request.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "id": 1,
            "path": "test/path",
            "description": "Test function",
            "instructions": "Do something",
        },
    )
    client = Client(api_key="op-dev-api-key", api_url="http://localhost:8000")
    function_description = client.functions.get_function_by_path("test/path")
    assert function_description.id == 1
    assert function_description.path == "test/path"
    assert function_description.description == "Test function"
    mock_do_request.assert_called_once_with(
        "GET",
        "/api/v1/functions/by_path/test/path",
    )


@pytest.mark.asyncio
@patch("opperai._http_clients._http_client.do_request")
async def test_get_function_by_id(mock_do_request):
    mock_do_request.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "id": 1,
            "path": "test/path",
            "description": "Test function",
            "instructions": "Do something",
        },
    )
    client = Client(api_key="op-dev-api-key", api_url="http://localhost:8000")
    function_description = client.functions.get_function_by_id("1")
    assert function_description.id == 1
    assert function_description.path == "test/path"
    assert function_description.description == "Test function"
    mock_do_request.assert_called_once_with(
        "GET",
        "/api/v1/functions/1",
    )
