class APIError(Exception):
    pass


class OpperTimeoutError(Exception):
    pass


class RateLimitError(Exception):
    pass


class StructuredGenerationError(Exception):
    pass
