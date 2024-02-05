from unittest.mock import MagicMock, patch

import pytest
from opperai import AsyncClient


@pytest.mark.asyncio
@patch("opperai._http_clients._async_http_client.do_request")
async def test_async_indexes_retrieve(mock_do_request):
    mock_do_request.return_value = MagicMock(
        status_code=200,
        json=lambda: [
            {
                "score": 2.3,
                "id": 1,
                "content": "Bonjour",
                "metadata": {"source": "test"},
            }
        ],
    )
    client = AsyncClient(api_key="op-dev-api-key", api_url="http://localhost:8000")
    resp = await client.indexes.retrieve(index_id=1, query="test", k=1)

    assert resp[0].content == "Bonjour"
    assert resp[0].metadata == {"source": "test"}
    mock_do_request.assert_called_once()
