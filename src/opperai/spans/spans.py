from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime

from opperai._client import Client
from opperai.types.spans import Span as SpanModel
from opperai.types.spans import SpanMetric


@dataclass
class Span:
    _client: Client
    uuid: str

    def update(self, **kwargs) -> "Span":
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
        span_uuid = self._client.spans.create(
            SpanModel(
                name=name,
                input=input,
                start_time=datetime.now(),
                parent_uuid=parent_span_id,
                meta=meta,
            )
        )
        span = Span(self._client, span_uuid)
        yield span
        span.update(end_time=datetime.now())
