from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, AsyncIterator, Dict, List

from opperai._client import AsyncClient
from opperai.core.spans import _current_span_id
from opperai.types.spans import GenerationIn, GenerationOut, SpanMetric
from opperai.types.spans import Span as SpanModel


@dataclass
class AsyncSpan:
    _client: AsyncClient
    _uuid: str

    @property
    def uuid(self) -> str:
        return self._uuid

    async def update(self, **kwargs) -> AsyncSpan:
        await self._client.spans.update(span_uuid=self._uuid, **kwargs)
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

    async def save_generation(
        self,
        duration_ms: int,
        called_at: datetime = None,
        input: str = None,
        response: str = None,
        model: str = None,
        messages: List[Dict[str, Any]] = None,
        prompt_tokens: int = None,
        completion_tokens: int = None,
        total_tokens: int = None,
        error: str = None,
        cost: float = None,
    ) -> GenerationOut:
        # if called_at is None, use the current time minus the duration_ms
        if called_at is None:
            now = datetime.now(timezone.utc)
            called_at = now - timedelta(milliseconds=duration_ms)

        return await self._client.spans.save_generation(
            uuid=self.uuid,
            generation=GenerationIn(
                called_at=called_at,
                duration_ms=duration_ms,
                input=input,
                response=response,
                model=model,
                messages=messages,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                error=error,
                cost=cost,
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
    ) -> AsyncIterator[AsyncSpan]:
        span = await self.start_span(name, input, meta, parent_span_id)
        try:
            yield span
        finally:
            await span.end()

    async def start_span(
        self,
        name: str,
        input: str = None,
        meta: dict = None,
        parent_span_id: str = None,
    ) -> AsyncSpan:
        span, token = await self._create_span(name, input, meta, parent_span_id)

        async def end_span():
            if not hasattr(span, "_ended"):
                await span.update(end_time=datetime.now(timezone.utc))
                _current_span_id.reset(token)
                span._ended = True

        span.end = end_span

        return span

    async def _create_span(self, name, input, meta, parent_span_id):
        parent_span_id = parent_span_id if parent_span_id else _current_span_id.get()
        span_model = await self._client.spans.create(
            SpanModel(
                name=name,
                input=input,
                start_time=datetime.now(timezone.utc),
                parent_uuid=parent_span_id,
                meta=meta,
            )
        )
        span = AsyncSpan(self._client, span_model.uuid)
        token = _current_span_id.set(str(span.uuid))

        return span, token

    @property
    def current_span(self) -> AsyncSpan:
        return AsyncSpan(self._client, _current_span_id.get())

    def get_span(self, span_id: str) -> AsyncSpan:
        return AsyncSpan(self._client, span_id)
