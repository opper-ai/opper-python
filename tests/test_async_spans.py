from contextlib import asynccontextmanager
from datetime import datetime

import pytest
from opperai import AsyncClient
from opperai.types.spans import Span, SpanMetric


@asynccontextmanager
async def span(desc: Span, _client: AsyncClient):
    _span = await _client.spans.create(desc)
    try:
        yield _span
    finally:
        await _client.spans.delete(_span.uuid)


@pytest.mark.asyncio
async def test_save_metric(aclient: AsyncClient):
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
        await aclient.spans.save_metric(
            _span.uuid, SpanMetric(dimension="dim", value=0.5, comment="comment")
        )
