import asyncio
from typing import List
from pydantic import BaseModel, Field
from opperai import Opper

import os

opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))


def bare_minimum():
    output = (
        opper.call(
            name="python/sdk/bare-minimum",
            instructions="answer the following question",
            input="what are some uses of 42",
        ),
    )
    print(output)


def stream_call():
    """Print the assistant’s answer as it streams back from Opper."""
    outer = opper.stream(
        name="python/sdk/bare-minimum-with-stream",
        instructions="answer the following question",
        input="what are some uses of 42",
    )

    # Pull out the inner EventStream object in one line.
    stream = next(value for key, value in outer if key == "result")

    # Read each Server-Sent Event and emit the delta text.
    for event in stream:  # event: ServerSentEvent
        delta = getattr(event.data, "delta", None)
        if delta:  # skip keep-alives, etc.
            print(delta, end="", flush=True)


def bare_minimum_with_model():
    output = opper.call(
        name="python/sdk/bare-minimum-with-model",
        instructions="answer the following question",
        input="what are some uses of 42",
        model="openai/gpt-4o-mini",
    )
    print(output)


def bare_minimum_with_fallbacks():
    output = opper.call(
        name="python/sdk/bare-minimum-with-fallbacks",
        instructions="answer the following question",
        input="what are some uses of 42",
        model=["openai/gpt-4o", "azure/gpt4-eu"],
    )
    print(output)


def bare_minimum_with_options():
    output = opper.call(
        name="python/sdk/bare-minimum-with-options",
        instructions="answer the following question",
        input="what are some uses of 42",
        model={"name": "openai/gpt-4.1-nano", "options": {"max_tokens": 5}},
    )
    print(output)


def bare_minimum_with_tags():
    output = opper.call(
        name="python/sdk/bare-minimum-with-tags",
        instructions="answer the following question",
        input=" what is the capital of france?",
        tags={"area": "world", "topic": "geography"},
    )
    print(output)


def structured_string_input_output():
    response_schema = {"type": "object", "properties": {"response": {"type": "string"}}}

    output = opper.call(
        name="python/sdk/structured-string-input-output",
        instructions="answer the following question",
        output_schema=response_schema,
        input=" what is the capital of france?",
    )
    print(output)


def structured_string_input_output_pydantic():
    class ModelResponse(BaseModel):
        response: str

    output = opper.call(
        name="python/sdk/structured-string-input-output",
        instructions="answer the following question",
        input=" what is the capital of france?",
        output_schema=ModelResponse,
    )
    print(output)


def structured_input_output():
    class Number(BaseModel):
        x: int

    class NumbersList(BaseModel):
        numbers: List[Number]

    output = opper.call(
        name="python/sdk/structured-input-output",
        instructions="given a list of numbers return the largest",
        input_schema=NumbersList,
        input=[Number(x=6), Number(x=7)],
        output_schema=Number,
    )
    print(output)


def call_with_examples():
    output = opper.call(
        name="python/sdk/call-with-examples",
        instructions="answer the following question",
        input="What is the most populated city in the world?",
        examples=[
            {
                "input": "what are some uses of 42",
                "output": "42 is the answer to the universe",
            },
            {"input": "what is the capital of france?", "output": "Paris"},
        ],
    )
    print(output)


def call_with_structured_examples():
    class Number(BaseModel):
        x: int = Field(..., ge=0, description="value of the number")

    class NumbersList(BaseModel):
        numbers: List[Number]

    output = opper.call(
        name="python/sdk/call-with-structured-examples",
        instructions="given a list of numbers return the largest",
        input_schema=NumbersList,
        input=[Number(x=1), Number(x=12)],
        output_schema=Number,
        examples=[
            {"input": [Number(x=1)], "output": Number(x=1), "comment": "small number"},
            {
                "input": [Number(x=2), Number(x=3)],
                "output": Number(x=3),
                "comment": "large number",
            },
        ],
    )
    print(output, end="\n\n")


CALLS = [
    ("Bare Minimum", bare_minimum),
    ("Stream Call", stream_call),
    ("Bare Minimum with Model", bare_minimum_with_model),
    ("Bare Minimum with Fallbacks", bare_minimum_with_fallbacks),
    ("Bare Minimum with Options", bare_minimum_with_options),
    ("Bare Minimum with Tags", bare_minimum_with_tags),
    ("Structured String Input Output", structured_string_input_output),
    (
        "Structured String Input Output Pydantic",
        structured_string_input_output_pydantic,
    ),
    ("Structured Input Output", structured_input_output),
    ("Call with Examples", call_with_examples),
    ("Call with Structured Examples", call_with_structured_examples),
]


def synchronous_calls():
    print("running synchronous calls:")
    for title, func in CALLS:
        print(f"\n{title}:")
        func()


# -----------------------------
# Asynchronous examples section
# -----------------------------


async def async_bare_minimum():
    output = await opper.call_async(
        name="python/sdk/bare-minimum",
        instructions="answer the following question",
        input="what are some uses of 42",
    )
    print(output)


async def async_stream_call() -> None:
    outer = await opper.stream_async(
        name="python/sdk/bare-minimum-with-stream",
        instructions="answer the following question",
        input="what are some uses of 42",
    )

    stream = next(value for key, value in outer if key == "result")

    async for event in stream:  # event: ServerSentEvent
        delta = getattr(event.data, "delta", None)
        if delta:
            print(delta, end="", flush=True)


async def async_bare_minimum_with_model():
    output = await opper.call_async(
        name="python/sdk/bare-minimum-with-model",
        instructions="answer the following question",
        input="what are some uses of 42",
        model="openai/gpt-4o-mini",
    )
    print(output)


async def async_bare_minimum_with_fallbacks():
    output = await opper.call_async(
        name="python/sdk/bare-minimum-with-fallbacks",
        instructions="answer the following question",
        input="what are some uses of 42",
        model=["openai/gpt-4o", "azure/gpt4-eu"],
    )
    print(output)


async def async_bare_minimum_with_options():
    output = await opper.call_async(
        name="python/sdk/bare-minimum-with-options",
        instructions="answer the following question",
        input="what are some uses of 42",
        model={"name": "openai/gpt-4.1-nano", "options": {"max_tokens": 5}},
    )
    print(output)


async def async_bare_minimum_with_tags():
    output = await opper.call_async(
        name="python/sdk/bare-minimum-with-tags",
        instructions="answer the following question",
        input=" what is the capital of france?",
        tags={"area": "world", "topic": "geography"},
    )
    print(output)


async def async_structured_string_input_output():
    response_schema = {"type": "object", "properties": {"response": {"type": "string"}}}

    output = await opper.call_async(
        name="python/sdk/structured-string-input-output",
        instructions="answer the following question",
        output_schema=response_schema,
        input=" what is the capital of france?",
    )
    print(output)


async def async_structured_string_input_output_pydantic():
    class ModelResponse(BaseModel):
        response: str

    output = await opper.call_async(
        name="python/sdk/structured-string-input-output",
        instructions="answer the following question",
        input=" what is the capital of france?",
        output_schema=ModelResponse,
    )
    print(output)


async def async_structured_input_output():
    class Number(BaseModel):
        x: int

    class NumbersList(BaseModel):
        numbers: List[Number]

    output = await opper.call_async(
        name="python/sdk/structured-input-output",
        instructions="given a list of numbers return the largest",
        input_schema=NumbersList,
        input=[Number(x=6), Number(x=7)],
        output_schema=Number,
    )
    print(output)


async def async_call_with_examples():
    output = await opper.call_async(
        name="python/sdk/call-with-examples",
        instructions="answer the following question",
        input="What is the most populated city in the world?",
        examples=[
            {
                "input": "what are some uses of 42",
                "output": "42 is the answer to the universe",
            },
            {"input": "what is the capital of france?", "output": "Paris"},
        ],
    )
    print(output)


async def async_call_with_structured_examples():
    class Number(BaseModel):
        x: int = Field(..., ge=0, description="value of the number")

    class NumbersList(BaseModel):
        numbers: List[Number]

    output = await opper.call_async(
        name="python/sdk/call-with-structured-examples",
        instructions="given a list of numbers return the largest",
        input_schema=NumbersList,
        input=[Number(x=1), Number(x=12)],
        output_schema=Number,
        examples=[
            {"input": [Number(x=1)], "output": Number(x=1), "comment": "small number"},
            {
                "input": [Number(x=2), Number(x=3)],
                "output": Number(x=3),
                "comment": "large number",
            },
        ],
    )
    print(output, end="\n\n")


ASYNC_CALLS = [
    async_bare_minimum,
    async_stream_call,
    async_bare_minimum_with_model,
    async_bare_minimum_with_fallbacks,
    async_bare_minimum_with_options,
    async_bare_minimum_with_tags,
    async_structured_string_input_output,
    async_structured_string_input_output_pydantic,
    async_structured_input_output,
    async_call_with_examples,
    async_call_with_structured_examples,
]


async def asynchronous_calls():
    print("running asynchronous calls:")

    await asyncio.gather(*(func() for func in ASYNC_CALLS))


if __name__ == "__main__":
    import sys

    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == "sync":
        synchronous_calls()
    elif arg == "async":
        asyncio.run(asynchronous_calls())
    else:
        synchronous_calls()
