# ruff: noqa: F401
from opperai.core.functions.decorator._decorator import fn, get_last_span_id
from opperai.core.spans._decorator import start_span, trace
from opperai.functions import Functions
from opperai.indexes import Indexes
from opperai.spans import Spans

from ._client import AsyncClient, Client


class Opper:
    client: Client = None

    functions: Functions = None
    indexes: Indexes = None
    spans: Spans = None

    def __init__(self, client: Client = None):
        if client is None:
            client = Client()

        self.client = client
        self.functions = Functions(client)
        self.indexes = Indexes(client)
        self.spans = Spans(client)
