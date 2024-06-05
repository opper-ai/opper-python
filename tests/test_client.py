from unittest.mock import patch

import httpx
import pytest
from opperai import AsyncOpper, Opper
from opperai._client import AsyncClient, Client
from opperai.types import Message
from opperai.types.exceptions import APIError, OpperTimeoutError


@pytest.mark.asyncio
async def test_async_client_raises_timeout_error(aclient: AsyncClient):
    async def mock_request(method, path, **kwargs):
        raise httpx.TimeoutException("request timed out")

    # with patch("opperai._client._get_project") as mock_get_project:
    #     mock_get_project.side_effect = lambda *args, **kwargs: Project(
    #         name="test", uuid="123e4567-e89b-12d3-a456-426614174000"
    #     )
    opper = AsyncOpper(client=aclient)
    f = await opper.functions.create("test_async_client_raises_timeout_error", "test")

    f._client.http_client.session.request = mock_request

    with pytest.raises(OpperTimeoutError):
        await f.chat(
            messages=[Message(role="user", content="say hello")],
        )

    with patch("opperai.core._http_clients.aconnect_sse") as mock_aconnect_sse:
        mock_aconnect_sse.side_effect = httpx.TimeoutException("request timed out")
        with pytest.raises(OpperTimeoutError):
            r = await f.chat(
                messages=[Message(role="user", content="say hello")],
                stream=True,
            )
            async for _ in r.deltas:
                pass


def test_client_raises_timeout_error(client: Client):
    def mock_request(method, path, **kwargs):
        raise httpx.TimeoutException("request timed out")

    opper = Opper(client=client)
    f = opper.functions.create("test_client_raises_timeout_error", "test")

    f._client.http_client.session.request = mock_request

    with pytest.raises(OpperTimeoutError):
        f.chat(messages=[Message(role="user", content="say hello")])

    with patch("opperai.core._http_clients.connect_sse") as mock_connect_sse:
        mock_connect_sse.side_effect = httpx.TimeoutException("request timed out")

        with pytest.raises(OpperTimeoutError):
            r = f.chat(
                messages=[Message(role="user", content="say hello")], stream=True
            )
            for _ in r:
                pass


def test_project_not_found(vcr_cassette):
    with pytest.raises(APIError):
        Client(project="not-a-real-project")
