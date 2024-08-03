import asyncio

from opperai import AsyncOpper, Opper, trace

opper = Opper()


def trace_with_context_manager():
    """trace using context manager"""

    with opper.trace.start(name="context manager") as span:
        span.save_metric("score", 100.0, "context manager")


def trace_manually():
    """trace manually using `start_span`"""

    span = opper.trace.start_span("manually created span")
    span.save_metric("score", 100.0, "manually created span")
    span.end()


@trace
def trace_with_decorator():
    """trace function using the `@trace` decorator"""

    opper.trace.current_span.save_metric("score", 100.0, "decorator")


@trace
def traced_chain():
    print("synchronous tracing")

    trace_with_context_manager()
    trace_manually()
    trace_with_decorator()

    opper.trace.current_span.save_metric("total_score", 100.0, "chain")


traced_chain()

aopper = AsyncOpper()


async def async_trace_with_context_manager():
    """trace using context manager"""

    async with aopper.trace.start(name="async context manager") as span:
        await span.save_metric("score", 100.0, "async context manager")


async def async_trace_manually():
    """trace manually using `start_span`"""

    span = await aopper.trace.start_span("manually created span")
    await span.save_metric("score", 100.0, "manually created span")
    await span.end()


@trace
async def async_trace_with_decorator():
    """trace function using the `@trace` decorator"""

    await aopper.trace.current_span.save_metric("score", 100.0, "decorator")


@trace
async def async_traced_chain():
    print("asynchronous tracing")

    await async_trace_with_context_manager()
    await async_trace_manually()
    await async_trace_with_decorator()

    await aopper.trace.current_span.save_metric("total_score", 100.0, "chain")


asyncio.run(async_traced_chain())
