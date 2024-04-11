import json
from uuid import UUID

from opperai._http_clients import _async_http_client
from opperai.types.spans import Span, SpanFeedback
from opperai.types.exceptions import APIError
from opperai.utils import DateTimeEncoder
from typing import Dict, Any


class AsyncSpans:
    def __init__(self, http_client: _async_http_client):
        self.http_client = http_client

    async def create(self, span: Span, **kwargs) -> Span:
        span_data = span.model_dump(exclude_none=True)
        json_payload = json.dumps(span_data, cls=DateTimeEncoder)
        response = await self.http_client.do_request(
            "POST",
            "/v1/spans",
            content=json_payload,
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to create span {span.name} with status {response.status_code}"
            )

        return Span.model_validate(response.json())

    async def update(self, span_uuid: UUID, **kwargs) -> Span:
        span = Span(uuid=span_uuid, **kwargs)
        json_payload = json.dumps(
            span.model_dump(exclude_none=True), cls=DateTimeEncoder
        )
        response = await self.http_client.do_request(
            "PUT",
            f"/v1/spans/{span.uuid}",
            content=json_payload,
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to update span `{span.name}` with status {response.status_code}"
            )

        return Span.model_validate(response.json())

    async def delete(self, span_uuid: UUID) -> bool:
        response = await self.http_client.do_request(
            "DELETE",
            f"/v1/spans/{span_uuid}",
        )
        if response.status_code != 204:
            raise APIError(
                f"Failed to update span `{span_uuid}` with status {response.status_code}"
            )

        return True

    async def save_example(self, uuid: str, **kwargs) -> Dict[str, Any]:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/spans/{uuid}/save_examples",
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to save examples for span {uuid} with status {response.status_code}"
            )

        return response.json()

    async def save_feedback(
        self, uuid: str, feedback: SpanFeedback, **kwargs
    ) -> Dict[str, Any]:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/spans/{uuid}/feedbacks",
            json=feedback.model_dump(exclude_unset=True),
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to add feedback for span {uuid} with status {response.status_code}"
            )

        return response.json()
