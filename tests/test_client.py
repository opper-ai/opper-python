from unittest.mock import patch

import httpx
import pytest
from opperai import AsyncOpper, Opper
from opperai._client import AsyncClient, Client
from opperai.types import Message
from opperai.types.exceptions import OpperTimeoutError


@pytest.mark.asyncio(scope="module")
async def test_async_client_raises_timeout_error(vcr_cassette):
    async def mock_request(method, path, **kwargs):
        raise httpx.TimeoutException("request timed out")

    opper = AsyncOpper(client=AsyncClient())
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


def test_client_raises_timeout_error(client: Client, vcr_cassette):
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
