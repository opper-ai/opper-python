from datetime import datetime
import pytest
from opperai.types.spans import Span, SpanFeedback
from opperai import AsyncClient
from contextlib import asynccontextmanager


@asynccontextmanager
async def span(desc: Span, _client: AsyncClient):
    _span = await _client.spans.create(desc)
    try:
        yield _span
    finally:
        await _client.spans.delete(_span.uuid)


@pytest.mark.asyncio(scope="module")
async def test_async_crud(aclient: AsyncClient, vcr_cassette):
    root_uuid = "bcf1b3b4-0b3b-4b3b-8b3b-0b3b4b3b4112"
    root_start_time = datetime(2021, 1, 1, 0, 0, 0, 0)
    root_end_time = datetime(2022, 1, 1, 0, 0, 0, 0)

    child_uuid = "cfc1c3c4-0c3c-4c3c-8c3c-0c3c4c31cc12"
    child_start_time = datetime(2021, 1, 1, 0, 0, 0, 0)
    child_end_time = datetime(2021, 12, 1, 0, 0, 0, 0)

    root_span = Span(
        uuid=root_uuid,
        project="project",
        name="name",
        input="input",
        start_time=root_start_time,
    )

    await aclient.spans.create(root_span)

    child_span = Span(
        uuid=child_uuid,
        parent_uuid=root_span.uuid,
        project="project",
        name="name",
        input="input",
        start_time=child_start_time,
    )

    await aclient.spans.create(child_span)

    await aclient.spans.update(
        child_span.uuid,
        end_time=child_end_time,
        output="output",
    )

    await aclient.spans.update(
        root_span.uuid,
        end_time=root_end_time,
        output="output",
    )

    assert await aclient.spans.delete(child_span.uuid)
    assert await aclient.spans.delete(root_span.uuid)


@pytest.mark.asyncio(scope="module")
async def test_save_feedback(aclient: AsyncClient, vcr_cassette):
    async with span(
        Span(
            uuid="bcf1b3b4-0b3b-4b3b-8b3b-0b3b4b3b4133",
            project="project",
            name="name",
            input="input",
            start_time=datetime(2021, 1, 1, 0, 0, 0, 0),
        ),
        aclient,
    ) as _span:
        await aclient.spans.save_feedback(
            _span.uuid, SpanFeedback(dimension="dim", score=0.5, comment="comment")
        )
