import pytest
from opperai.types import SpanMetric, validate_id_xor_path
from pydantic import ValidationError


def test_id_xor_path():
    @validate_id_xor_path
    def test_function(id=None, path=None):
        return id, path

    assert test_function(id=1) == (1, None)

    assert test_function(path="test") == (None, "test")

    with pytest.raises(ValueError):
        test_function(id=1, path="test")

    with pytest.raises(ValueError):
        test_function()

    with pytest.raises(ValueError):
        test_function(id=1, path="test", other="other")


def test_feedback_score_in_range():
    assert SpanMetric(score=0.5).score == 0.5
    assert SpanMetric(score=0).score == 0
    assert SpanMetric(score=1).score == 1
    with pytest.raises(ValidationError):
        SpanMetric(score=1.1)
    with pytest.raises(ValidationError):
        SpanMetric(score=-0.1)
