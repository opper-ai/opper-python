from opperai._http_clients import _async_http_client
from opperai.types.exceptions import APIError
from opperai.types.indexes import IndexRetrieveResponse


class AsyncIndexes:
    def __init__(self, http_client: _async_http_client):
        self.http_client = http_client

    async def retrieve(self, index_id: int, query: str, k: int):
        response = await self.http_client.do_request(
            "POST",
            f"/v1/indexes/{index_id}/query",
            json={"q": query, "k": k},
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to retrieve index {index_id} with status {response.status_code}"
            )
        return [IndexRetrieveResponse.model_validate(item) for item in response.json()]
