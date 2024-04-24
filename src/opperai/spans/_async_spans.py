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
        """
        Saves a span as an positive example.

        This method sends a POST request to the server's `/v1/spans/{uuid}/save_examples` endpoint.
        The UUID in the URL is replaced with the UUID of the span for which the example is being saved.

        Args:
            uuid (str): The UUID of the span for which the example is being saved 
            **kwargs: Additional keyword arguments that can be used for future extensions or to include additional data
                    in the request. These are not used in the current implementation.

        Returns:
            Dict[str, Any]: A dictionary containing the server's response. The structure of this dictionary is determined
                            by the server's response schema for the save example endpoint.

        Raises:
            APIError: If the server responds with a status code other than 200, indicating that the example was not
                    successfully saved for the span.

        Examples:
            >>> from opperai import Client
            >>> opper = Client()
            >>> span_uuid = "123e4567-e89b-12d3-a456-426614174000"
            >>> result = await opper.spans.save_example(span_uuid)
            >>> print(result)
        """
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
        """
        Saves feedback for a specific span.

        This method sends a POST request to the server's `/v1/spans/{uuid}/feedbacks` endpoint, including the feedback data
        for the span identified by the given UUID. The feedback data is serialized into JSON format, excluding any unset
        attributes, before being sent as the request payload.

        Args:
            uuid (str): The UUID of the span for which feedback is being saved.
            feedback (SpanFeedback): The feedback object containing the feedback data for the span.
            **kwargs: Additional keyword arguments that can be used for future extensions or to include additional data
                    in the request. These are not used in the current implementation.

        Returns:
            Dict[str, Any]: A dictionary containing the server's response. The structure of this dictionary is determined
                            by the server's response schema for the feedback submission endpoint.

        Raises:
            APIError: If the server responds with a status code other than 200, indicating that the feedback was not
                    successfully saved for the span.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types.spans import SpanFeedback
            >>> opper = Client()
            >>> feedback = SpanFeedback(rating=5, comment="Very accurate")
            >>> span_uuid = "123e4567-e89b-12d3-a456-426614174000"
            >>> result = await opper.spans.save_feedback(span_uuid, feedback)
            >>> print(result)
        """
        
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
