from typing import List, Optional

from opperai.core._http_clients import _http_client
from opperai.types import Project


class Projects:
    def __init__(self, http_client: _http_client):
        self.http_client = http_client

    def list(self) -> List[Project]:
        response = self.http_client.do_request(
            "GET",
            "/v1/projects",
        )

        return [
            Project(
                uuid=project["uuid"],
                name=project["name"],
            )
            for project in response.json()
        ]

    def get(
        self, name: Optional[str] = None, uuid: Optional[str] = None
    ) -> Optional[Project]:
        if name:
            for project in self.list():
                if project.name == name:
                    return project
        elif uuid:
            for project in self.list():
                if project.uuid == uuid:
                    return project

        return None
