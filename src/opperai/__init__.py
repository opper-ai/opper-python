# ruff: noqa: F401
from dataclasses import dataclass

from opperai.core.functions.decorator._decorator import fn, get_last_span_id
from opperai.core.spans._decorator import start_span, trace
from opperai.functions import Functions
from opperai.indexes import Indexes
from opperai.spans import Spans

from ._client import AsyncClient, Client


@dataclass
class Opper:
    client: Client = Client()

    functions: Functions = None
    indexes: Indexes = None
    spans: Spans = None

    def __post_init__(self):
        self.functions = Functions(self.client)
        self.indexes = Indexes(self.client)
        self.spans = Spans(self.client)
