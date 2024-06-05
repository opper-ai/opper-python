from unittest.mock import patch

from opperai import Client, trace


def test_trace_decorator(client: Client, vcr_cassette):
    span_uuid = "123e4567-e89b-12d3-a456-426614174002"
    with patch("opperai.core.spans._decorator.uuid4") as mock_uuid:
        mock_uuid.return_value = span_uuid
        with patch("opperai.core.spans._decorator.utcnow") as mock_utcnow:
            mock_utcnow.return_value = "2024-01-01 00:00:00"

            @trace(client=client)
            def something(text: str, target_language: str) -> str:
                return "Hola"

            assert something("Hello", "es") == "Hola"

        client.spans.delete(span_uuid)
