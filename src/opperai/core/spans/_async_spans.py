import json
from typing import Any, Dict
from uuid import UUID

from opperai.core._http_clients import _async_http_client
from opperai.core.utils import DateTimeEncoder
from opperai.types.exceptions import APIError
from opperai.types.spans import GenerationIn, GenerationOut, Span, SpanMetric


class AsyncSpans:
    def __init__(self, http_client: _async_http_client):
        self.http_client = http_client

    async def create(self, span: Span, **kwargs) -> Span:
        """Create a new span in the system

        This method sends a POST request to the server to create a new span with the provided details. The span's data is serialized into JSON format, excluding any unset attributes, before being sent as the request payload.

        Args:
            span (Span): An instance of the Span class, representing the span to be created.
            **kwargs: Additional keyword arguments that will be included in the request payload.

        Returns:
            Span: An instance of the Span class, representing the newly created span, including its server-assigned UUID and any other relevant information.

        Raises:
            APIError: If the span creation fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types.spans import Span
            >>> client = Client(api_key="your_api_key_here")
            >>> new_span = Span(
            ...     name="New Span",
            ...     start_time="2021-07-21T17:32:28Z",
            ...     end_time="2021-07-21T18:32:28Z",
            ...     metadata={"key": "value"}
            ... )
            >>> created_span = asyncio.run(client.spans.create(new_span))
            >>> print(created_span)
            Span(uuid='123e4567-e89b-12d3-a456-426614174000', name='New Span', ...)
        """
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
        """Update an existing span in the system

        This method sends a PUT request to the server to update an existing span identified by its UUID with the provided details. The span's data is serialized into JSON format, excluding any unset attributes, before being sent as the request payload.

        Args:
            span_uuid (UUID): The UUID of the span to be updated.
            **kwargs: Additional keyword arguments that will be included in the request payload.

        Returns:
            Span: An instance of the Span class, representing the updated span, including its server-assigned UUID and any other relevant information.

        Raises:
            APIError: If the span update fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types.spans import Span
            >>> client = Client(api_key="your_api_key_here")
            >>> updated_span = Span(
            ...     name="Updated Span",
            ...     start_time="2021-07-21T17:32:28Z",
            ...     end_time="2021-07-21T18:32:28Z",
            ...     metadata={"key": "new_value"}
            ... )
            >>> result = asyncio.run(client.spans.update("123e4567-e89b-12d3-a456-426614174000", updated_span))
            >>> print(result)
            Span(uuid='123e4567-e89b-12d3-a456-426614174000', name='Updated Span', ...)
        """
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
        """Delete an existing span from the system

        This method sends a DELETE request to the server to remove a span identified by its UUID. If the deletion is successful, the method returns True, indicating that the span has been successfully removed from the system.

        Args:
            span_uuid (UUID): The UUID of the span to be deleted.

        Returns:
            bool: True if the span was successfully deleted, False otherwise.

        Raises:
            APIError: If the span deletion fails due to an API error.

        Examples:
            >>> from opperai import Client
            >>> client = Client(api_key="your_api_key_here")
            >>> span_uuid = "123e4567-e89b-12d3-a456-426614174000"
            >>> result = asyncio.run(client.spans.delete(span_uuid))
            >>> print(result)
            True
        """
        response = await self.http_client.do_request(
            "DELETE",
            f"/v1/spans/{span_uuid}",
        )
        if response.status_code != 204:
            raise APIError(
                f"Failed to delete span `{span_uuid}` with status {response.status_code}"
            )

        return True

    async def save_example(self, uuid: str, **kwargs) -> Dict[str, Any]:
        """Saves a span as an positive example

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

    async def save_metric(
        self, uuid: str, metric: SpanMetric, **kwargs
    ) -> Dict[str, Any]:
        """Saves metric for a specific span

        This method sends a POST request to the server's `/v1/spans/{uuid}/metrics` endpoint, including the metric data
        for the span identified by the given UUID. The metric data is serialized into JSON format, excluding any unset
        attributes, before being sent as the request payload.

        Args:
            uuid (str): The UUID of the span for which metric is being saved.
            metric (SpanMetric): The metric object containing the metric data for the span.
            **kwargs: Additional keyword arguments that can be used for future extensions or to include additional data
                    in the request. These are not used in the current implementation.

        Returns:
            Dict[str, Any]: A dictionary containing the server's response. The structure of this dictionary is determined
                            by the server's response schema for the metric submission endpoint.

        Raises:
            APIError: If the server responds with a status code other than 200, indicating that the metric was not
                    successfully saved for the span.

        Examples:
            >>> from opperai import Client
            >>> from opperai.types.spans import SpanMetric
            >>> opper = Client()
            >>> metric = SpanMetric(name="accuracy", value=0.9)
            >>> span_uuid = "123e4567-e89b-12d3-a456-426614174000"
            >>> result = await opper.spans.save_metric(span_uuid, metric)
            >>> print(result)
        """

        response = await self.http_client.do_request(
            "POST",
            f"/v1/spans/{uuid}/metrics",
            json=metric.model_dump(exclude_unset=True),
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to add metric for span {uuid} with status {response.status_code}"
            )

        return response.json()

    async def save_generation(
        self,
        uuid: str,
        generation: GenerationIn,
    ) -> GenerationOut:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/spans/{uuid}/generation",
            content=json.dumps(
                generation.model_dump(exclude_none=True), cls=DateTimeEncoder
            ),
        )

        if response.status_code != 200:
            raise APIError(
                f"Failed to save generation for span {uuid} with status {response.status_code}"
            )

        return GenerationOut.model_validate(response.json())
