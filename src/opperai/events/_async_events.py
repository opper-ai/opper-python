import json

from opperai._http_clients import _http_client
from opperai.types.events import Event, EventFeedback
from opperai.types.exceptions import APIError
from opperai.utils import DateTimeEncoder


class AsyncEvents:
    def __init__(self, http_client: _http_client):
        self.http_client = http_client

    async def create(self, event: Event, **kwargs) -> str:
        event_data = event.model_dump(exclude_none=True)
        json_payload = json.dumps(event_data, cls=DateTimeEncoder)
        response = await self.http_client.do_request(
            "POST",
            "/v1/events",
            data=json_payload,
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to create event {event.name} with status {response.status_code}"
            )

        return response.json()["uuid"]

    async def update(self, event: Event, **kwargs) -> str:
        json_payload = json.dumps(
            event.model_dump(exclude_none=True), cls=DateTimeEncoder
        )
        response = await self.http_client.do_request(
            "PUT",
            f"/v1/events/{event.uuid}",
            data=json_payload,
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to update event `{event.name}` with status {response.status_code}"
            )

        return response.json()["uuid"]

    async def save_example(self, uuid: str, **kwargs) -> str:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/events/{uuid}/save_examples",
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to save examples for event {uuid} with status {response.status_code}"
            )

        return response.json()["uuid"]

    async def save_feedback(self, uuid: str, feedback: EventFeedback, **kwargs) -> str:
        response = await self.http_client.do_request(
            "POST",
            f"/v1/events/{uuid}/feedbacks",
            json=feedback.model_dump(exclude_unset=True),
        )
        if response.status_code != 200:
            raise APIError(
                f"Failed to add feedback for event {uuid} with status {response.status_code}"
            )

        return response.json()
