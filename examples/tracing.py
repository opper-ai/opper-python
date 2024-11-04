"""Demonstrate how to capture execution traces.

Each method demonstrates how to capture execution traces using different methods.
It also demonstrates how to add metrics and manual generations to the traces.
Generations are added automatically when using `opper.call` or when functions created
with `opper.functions.create` or `@fn` are called.
"""

import asyncio
import time

from opperai import AsyncOpper, Opper, trace

opper = Opper()


def trace_with_context_manager():
    """trace using context manager"""

    with opper.traces.start(name="context manager") as span:
        span.save_metric("score", 100.0, "context manager")


def trace_manually():
    """trace manually using `start_span`"""

    span = opper.traces.start_span("manually created span")
    span.save_metric("score", 100.0, "manually created span")

    span.end()


@trace
def trace_with_decorator():
    """trace function using the `@trace` decorator"""

    opper.traces.current_span.save_metric("score", 100.0, "decorator")


def manual_generation():
    """manually add a generation to the current span"""

    with opper.traces.start(
        name="manual generation",
        input="What is the meaning of life?",
    ) as span:
        time.sleep(0.1)
        span.save_generation(
            duration_ms=100,
            input="What is the meaning of life?",
            response="42",
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the meaning of life?"},
                {"role": "assistant", "content": "42"},
            ],
        )


@trace
def trace_with_call():
    result, response = opper.call(name="python/sdk/bare-minimum", input="Hello, world!")
    response.span.save_metric("score", 100.0, "call")

    return result


def get_span_and_save_metric():
    # Create span during runtime
    span = opper.traces.start_span("async_get_span_and_save_metric")
    span.end()
    span_id = span.uuid

    # Later fetch the span using its uuid and save a metric
    metric_span = opper.spans.get_span(span_id=span_id)
    metric_span.save_metric("my_metric", 1, "my metric comment")


@trace
def run_sync():
    print("running synchronous tracing")

    trace_with_context_manager()
    trace_manually()
    trace_with_decorator()
    manual_generation()
    trace_with_call()
    get_span_and_save_metric()

    opper.traces.current_span.save_metric(
        "total_score", 100.0, "metric on the root span"
    )


aopper = AsyncOpper()


async def async_trace_with_context_manager():
    """trace using context manager"""

    async with aopper.traces.start(name="async context manager") as span:
        await span.save_metric("score", 100.0, "async context manager")


async def async_trace_manually():
    """trace manually using `start_span`"""

    span = await aopper.traces.start_span("manually created span")
    await span.save_metric("score", 100.0, "manually created span")
    await span.end()


@trace
async def async_trace_with_decorator():
    """trace function using the `@trace` decorator"""

    await aopper.traces.current_span.save_metric("score", 100.0, "decorator")


async def async_manual_generation():
    """manually add a generation to the current span"""

    async with aopper.traces.start(
        name="async manual generation",
        input="What is the meaning of life?",
    ) as span:
        time.sleep(0.1)
        await span.save_generation(
            duration_ms=100,
            input="What is the meaning of life?",
            response="42",
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the meaning of life?"},
                {"role": "assistant", "content": "42"},
            ],
        )


@trace
async def async_trace_with_call():
    result, response = await aopper.call(
        name="python/sdk/bare-minimum", input="Hello, world!"
    )
    await response.span.save_metric("score", 100.0, "call")

    return result


async def async_get_span_and_save_metric():
    # Create span during runtime
    span = await aopper.traces.start_span("async_get_span_and_save_metric")
    await span.end()
    span_id = span.uuid

    # Later fetch the span using its uuid and save a metric
    metric_span = aopper.spans.get_span(span_id=span_id)
    await metric_span.save_metric("my_metric", 1, "my metric comment")


@trace
async def run_async():
    print("running asynchronous tracing")

    await asyncio.gather(
        async_trace_with_context_manager(),
        async_trace_manually(),
        async_trace_with_decorator(),
        async_manual_generation(),
        async_trace_with_call(),
        async_get_span_and_save_metric(),
    )

    await aopper.traces.current_span.save_metric("total_score", 100.0, "chain")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        if sys.argv[1] == "async":
            asyncio.run(run_async())
        elif sys.argv[1] == "sync":
            run_sync()
    else:
        run_sync()
        asyncio.run(run_async())
