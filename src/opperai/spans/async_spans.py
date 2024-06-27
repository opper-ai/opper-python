from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime

from opperai._client import AsyncClient
from opperai.types.spans import Span as SpanModel
from opperai.types.spans import SpanMetric


@dataclass
class AsyncSpan:
    _client: AsyncClient
    _uuid: str

    @property
    def uuid(self) -> str:
        return self._uuid

    async def update(self, **kwargs) -> "AsyncSpan":
        self._client.spans.update(span_uuid=self._uuid, **kwargs)
        return self

    async def delete(self) -> bool:
        return await self._client.spans.delete(span_uuid=self._uuid)

    async def save_example(self, **kwargs) -> str:
        return await self._client.spans.save_example(uuid=self._uuid, **kwargs)

    async def save_metric(
        self, dimension: str, value: float, comment: str = None
    ) -> bool:
        return await self._client.spans.save_metric(
            uuid=self._uuid,
            metric=SpanMetric(
                dimension=dimension,
                value=value,
                comment=comment,
            ),
        )


class AsyncSpans:
    _client: AsyncClient = None

    def __init__(self, client: AsyncClient = None):
        if client is None:
            client = AsyncClient()

        self._client = client

    @asynccontextmanager
    async def start(
        self,
        name: str,
        input: str = None,
        meta: dict = None,
        parent_span_id: str = None,
    ) -> AsyncSpan:
        uuid = self._client.spans.create(
            SpanModel(
                name=name,
                input=input,
                start_time=datetime.now(),
                parent_uuid=parent_span_id,
                meta=meta,
            )
        )
        span = AsyncSpan(self._client, uuid)
        yield span
        await span.update(end_time=datetime.now())
