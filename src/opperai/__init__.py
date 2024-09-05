# ruff: noqa: F401
from opperai.core.spans._decorator import start_span, trace
from opperai.functions.async_functions import AsyncFunctions
from opperai.functions.decorator._decorator import fn, get_last_span_id
from opperai.functions.functions import Functions
from opperai.indexes.async_indexes import AsyncIndexes
from opperai.indexes.indexes import Index, Indexes
from opperai.spans.async_spans import AsyncSpans
from opperai.spans.spans import Spans

from .__version__ import __version__
from ._client import AsyncClient, Client
from ._opper import AsyncOpper, Opper
