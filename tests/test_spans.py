from datetime import datetime
from opperai.types.spans import Span
from opperai import Client


def test_crud(client: Client, vcr_cassette):
    root_uuid = "bcf1b3b4-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
    root_start_time = datetime(2021, 1, 1, 0, 0, 0, 0)
    root_end_time = datetime(2022, 1, 1, 0, 0, 0, 0)

    child_uuid = "cfc1c3c4-0c3c-4c3c-8c3c-0c3c4c3c4c3c"
    child_start_time = datetime(2021, 1, 1, 0, 0, 0, 0)
    child_end_time = datetime(2021, 12, 1, 0, 0, 0, 0)

    root_span = Span(
        uuid=root_uuid,
        project="project",
        name="name",
        input="input",
        start_time=root_start_time,
    )

    client.spans.create(root_span)

    child_span = Span(
        uuid=child_uuid,
        parent_uuid=root_span.uuid,
        project="project",
        name="name",
        input="input",
        start_time=child_start_time,
    )

    client.spans.create(child_span)

    client.spans.update(
        child_span.uuid,
        end_time=child_end_time,
        output="output",
    )

    client.spans.update(
        root_span.uuid,
        end_time=root_end_time,
        output="output",
    )

    assert client.spans.delete(child_span.uuid)
    assert client.spans.delete(root_span.uuid)
