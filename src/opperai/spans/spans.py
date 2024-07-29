from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from opperai._client import Client
from opperai.core.spans import _current_span_id
from opperai.types.spans import GenerationIn, GenerationOut, SpanMetric
from opperai.types.spans import Span as SpanModel


@dataclass
class Span:
    _client: Client
    uuid: str

    def update(self, **kwargs) -> Span:
        self._client.spans.update(span_uuid=self.uuid, **kwargs)
        return self

    def delete(self) -> bool:
        return self._client.spans.delete(span_uuid=self.uuid)

    def save_example(self, **kwargs) -> str:
        return self._client.spans.save_example(uuid=self.uuid, **kwargs)

    def save_metric(self, dimension: str, value: float, comment: str = None) -> bool:
        return self._client.spans.save_metric(
            uuid=self.uuid,
            metric=SpanMetric(
                dimension=dimension,
                value=value,
                comment=comment,
            ),
        )

    def save_generation(
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

        return self._client.spans.save_generation(
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


class Spans:
    _client: Client = None

    def __init__(self, client: Client = None):
        if client is None:
            client = Client()

        self._client = client

    @contextmanager
    def start(
        self,
        name: str,
        input: str = None,
        meta: dict = None,
        parent_span_id: str = None,
    ) -> Span:
        parent_span_id = parent_span_id if parent_span_id else _current_span_id.get()
        span = self._client.spans.create(
            SpanModel(
                name=name,
                input=input,
                start_time=datetime.now(timezone.utc),
                parent_uuid=parent_span_id,
                meta=meta,
            )
        )
        span = Span(self._client, span.uuid)
        span_token = _current_span_id.set(str(span.uuid))
        try:
            yield span
        finally:
            span.update(end_time=datetime.now(timezone.utc))
            _current_span_id.reset(span_token)
