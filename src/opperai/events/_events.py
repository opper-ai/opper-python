import json
from uuid import UUID

from opperai._http_clients import _http_client
from opperai.types.events import Event
from opperai.types.exceptions import APIError
from opperai.utils import DateTimeEncoder


class Events:
    def __init__(self, http_client: _http_client):
        self.http_client = http_client

    def create(self, event: Event, **kwargs) -> str:
        event_data = event.model_dump(exclude_none=True)
        json_payload = json.dumps(event_data, cls=DateTimeEncoder)
        response = self.http_client.do_request(
            "POST",
            "/v1/events",
            data=json_payload,
        )
        if response.status_code != 200:
            print(response.json())
            raise APIError(
                f"Failed to create event {event.name} with status {response.status_code}"
            )
        return response.json()["uuid"]

    def update(self, event_uuid: UUID, **kwargs) -> str:
        event = Event(uuid=event_uuid, **kwargs)
        json_payload = json.dumps(
            event.model_dump(exclude_none=True), cls=DateTimeEncoder
        )
        response = self.http_client.do_request(
            "PUT",
            f"/v1/events/{event.uuid}",
            data=json_payload,
        )
        if response.status_code != 200:
            print(response.json())
            raise APIError(
                f"Failed to update event `{event.name}` with status {response.status_code}"
            )

        return response.json()["uuid"]
