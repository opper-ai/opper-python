import contextvars

_current_span_id = contextvars.ContextVar("_current_span_id", default=None)


def get_current_span_id():
    return _current_span_id.get()
