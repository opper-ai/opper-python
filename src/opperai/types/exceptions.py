from typing import Optional


class APIError(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class OpperBaseException(Exception):
    """Base class for all exceptions raised by the opperai API."""

    type: Optional[str] = None
    message: Optional[str] = None
    detail: Optional[str] = None

    def __init__(
        self,
        type: Optional[str] = None,
        message: Optional[str] = None,
        detail: Optional[str] = None,
    ):
        super().__init__(message)
        self.type = type if type else self.type
        self.message = message if message else self.message
        self.detail = detail if detail else self.detail


class OpperTimeoutError(OpperBaseException):
    """Raised when the request to the opper api times out."""

    type: str = "OpperTimeoutError"


class RateLimitError(OpperBaseException):
    """Raised when the rate limit is exceeded."""

    type: str = "RateLimitError"


class StructuredGenerationError(OpperBaseException):
    """Raised when the structured generation fails."""

    type: str = "StructuredGenerationError"


class ContentPolicyViolationError(OpperBaseException):
    """Raised when the content policy is violated."""

    type: str = "ContentPolicyViolationError"


class RequestValidationError(OpperBaseException):
    """Raised when the request validation fails."""

    type: str = "RequestValidationError"
