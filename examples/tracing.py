import time
import os

from opperai import Opper

opper = Opper(os.getenv("OPPER_API_KEY"))


def create_span():
    span = opper.spans.create(
        name="my_span", start_time=time.time(), type="workflow"
    )
    print("Created parent span: ")
    print(span)
    return span


def make_call(parent_span_id: str):
    # A call gets its own span but you can make it a child of a parent span
    response = opper.call(
        name="my_call",
        instructions="Answer the question",
        input="What is half the half of double the number 10?",
        model="openai/gpt-4.1-nano",
        parent_span_id=parent_span_id,
    )
    print(response)
    return response.json_payload


def update_span(span_id: str):
    opper.spans.update(span_id=span_id, end_time=time.time())


def save_metric(span_id: str, value: int, comment: str):
    opper.span_metrics.create_metric(
        span_id=span_id, dimension="score", value=value
    )

def save_span_to_datasets(span_id: str):
    opper.spans.save_examples(span_id=span_id)


def get_trace(trace_id: str):
    trace = opper.traces.get(trace_id=trace_id)
    print(trace)


if __name__ == "__main__":
    parent_span = create_span()
    start_time = time.time()
    make_call(parent_span.id)
    end_time = time.time()
    # We want to measure if the call is fast. Less than 3s is score=1, else 0

    if end_time - start_time < 3: # considered success
        save_metric(parent_span.id, 1, f"Total time: {end_time - start_time}")
        # If successful we save the example
        save_span_to_datasets(parent_span.id)
    else:
        save_metric(parent_span.id, 0, f"Total time: {end_time - start_time}")

    update_span(parent_span.id)

    # Get the trace
    print("Getting trace...")
    trace = get_trace(parent_span.trace_id)
    print(trace)

