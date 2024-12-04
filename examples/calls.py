import asyncio
from typing import List

from pydantic import BaseModel, Field

from opperai import AsyncOpper, Opper, trace
from opperai.types import CallConfiguration, Example

opper = Opper()


def stream_call():
    res = opper.call(
        name="python/sdk/stream_call",
        instructions="answer the following question",
        input="what are some uses of 42",
        stream=True,
        configuration=CallConfiguration(
            model_parameters={
                "max_tokens": 100,
            }
        ),
    )
    for chunk in res.deltas:
        print(chunk)


@trace
def bare_minimum():
    output, _ = opper.call(
        name="python/sdk/bare-minimum",
        instructions="answer the following question",
        input="what are some uses of 42",
        configuration=CallConfiguration(
            model_parameters={
                "max_tokens": 10,
            }
        ),
    )
    print(output)


@trace
def bare_minimum_with_model():
    output, _ = opper.call(
        name="python/sdk/bare-minimum-with-model",
        instructions="answer the following question",
        input="what are some uses of 42",
        model="mistral/mistral-tiny-eu",
        configuration=CallConfiguration(
            model_parameters={
                "max_tokens": 10,
            }
        ),
    )
    print(output)


@trace
def structured_string_input_output():
    class Number(BaseModel):
        x: int

    output, _ = opper.call(
        name="python/sdk/structured-input-output",
        instructions="given a word, translate it to spanish",
        input="hello",
        output_type=str,
    )
    print(output)


@trace
def structured_input_output():
    class Number(BaseModel):
        x: int

    output, _ = opper.call(
        name="python/sdk/structured-input-output",
        instructions="given a list of numbers return the largest",
        input=[Number(x=6), Number(x=7)],
        output_type=Number,
    )
    print(output)


@trace
def call_with_examples():
    output, _ = opper.call(
        name="python/sdk/call-with-examples",
        instructions="extract the weekday from a text",
        examples=[
            Example(input="Today is Monday", output="Monday"),
            Example(input="Friday is the best day of the week", output="Friday"),
            Example(
                input="Saturday is the second best day of the week", output="Saturday"
            ),
        ],
        input="Wonder what day it is on Sunday",
    )
    print(output)


@trace
def call_with_structured_examples():
    class Number(BaseModel):
        x: int = Field(..., ge=0, description="value of the number")

    output, _ = opper.call(
        name="python/sdk/call-with-structured-examples",
        instructions="given a list of numbers return the largest",
        input_type=List[Number],
        input=[Number(x=1), Number(x=12)],
        output_type=Number,
        examples=[
            Example(input=[Number(x=1)], output=Number(x=1)),
            Example(input=[Number(x=2), Number(x=3)], output=Number(x=3)),
        ],
    )
    print(output)


@trace
def bare_minimum_with_fallbacks():
    output, _ = opper.call(
        name="python/sdk/bare-minimum-with-fallbacks",
        instructions="answer the following question",
        input="what are some uses of 42",
        model="azure/gpt4-eu",
        fallback_models=["openai/gpt-4o", "openai/gpt-3.5-turbo"],
        configuration=CallConfiguration(
            model_parameters={
                "max_tokens": 10,
            }
        ),
    )
    print(output)


@trace
def call_with_tags():
    output, _ = opper.call(
        name="python/sdk/call-with-tags",
        instructions="answer the following question",
        input="what are some uses of 42",
        tags={"customer": "x"},
    )
    print(output)


@trace
def synchronous_call():
    print("running synchronous calls")
    bare_minimum()
    bare_minimum_with_model()
    structured_input_output()
    call_with_structured_examples()
    call_with_examples()
    structured_string_input_output()
    stream_call()
    bare_minimum_with_fallbacks()
    call_with_tags()


aopper = AsyncOpper()


@trace
async def async_bare_minimum():
    output, _ = await aopper.call(
        name="python/sdk/async-bare-minimum",
        instructions="answer the following question",
        input="what are some uses of 42",
        configuration=CallConfiguration(
            model_parameters={
                "max_tokens": 10,
            }
        ),
    )
    print(output)


@trace
async def async_bare_minimum_with_model():
    output, _ = await aopper.call(
        name="python/sdk/async-bare-minimum-with-model",
        instructions="answer the following question",
        input="what are some uses of 42",
        model="mistral/mistral-tiny-eu",
    )
    print(output)


@trace
async def async_bare_minimum_with_fallbacks():
    output, _ = await aopper.call(
        name="python/sdk/async-bare-minimum-with-fallbacks",
        instructions="answer the following question",
        input="what are some uses of 42",
        model="azure/gpt4-eu",
        fallback_models=["openai/gpt-4", "openai/gpt-3.5-turbo"],
        configuration=CallConfiguration(
            model_parameters={
                "max_tokens": 10,
            }
        ),
    )
    print(output)


@trace
async def async_structured_string_input_output():
    output, _ = await aopper.call(
        name="python/sdk/async-structured-string-input-output",
        instructions="given a word, translate it to spanish",
        input="hello",
        output_type=str,
    )
    print(output)


@trace
async def async_structured_input_output():
    class Number(BaseModel):
        x: int

    output, _ = await aopper.call(
        name="python/sdk/async-structured-input-output",
        instructions="given a list of numbers return the largest",
        input=[Number(x=6), Number(x=7)],
        output_type=Number,
    )
    print(output)


@trace
async def async_call_with_examples():
    output, _ = await aopper.call(
        name="python/sdk/async-call-with-examples",
        instructions="extract the weekday from a text",
        examples=[
            Example(input="Today is Monday", output="Monday"),
            Example(input="Friday is the best day of the week", output="Friday"),
            Example(
                input="Saturday is the second best day of the week", output="Saturday"
            ),
        ],
        input="Wonder what day it is on Sunday",
        configuration=CallConfiguration(
            model_parameters={
                "max_tokens": 10,
            }
        ),
    )
    print(output)


@trace
async def async_call_with_structured_examples():
    class Number(BaseModel):
        x: int = Field(..., ge=0, description="value of the number")

    output, _ = await aopper.call(
        name="python/sdk/async-call-with-structured-examples",
        instructions="given a list of numbers return the largest",
        input_type=List[Number],
        input=[Number(x=1), Number(x=12)],
        output_type=Number,
        examples=[
            Example(input=[Number(x=1)], output=Number(x=1)),
            Example(input=[Number(x=2), Number(x=3)], output=Number(x=3)),
        ],
    )
    print(output)


@trace
async def async_stream_call():
    aopper = AsyncOpper()
    res = await aopper.call(
        name="python/sdk/async-stream-call",
        instructions="answer the following question",
        input="what are some uses of 42",
        stream=True,
    )
    async for chunk in res.deltas:
        print(chunk)


@trace
async def async_call_with_tags():
    output, _ = await aopper.call(
        name="python/sdk/async-call-with-tags",
        instructions="answer the following question",
        input="what are some uses of 42",
        tags={"customer": "x"},
    )
    print(output)


@trace
async def async_call():
    print("running asynchronous calls")
    await asyncio.gather(
        async_bare_minimum(),
        async_bare_minimum_with_model(),
        async_bare_minimum_with_fallbacks(),
        async_structured_input_output(),
        async_call_with_examples(),
        async_call_with_structured_examples(),
        async_structured_string_input_output(),
        async_stream_call(),
        async_call_with_tags(),
    )


if __name__ == "__main__":
    import sys

    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == "sync":
        synchronous_call()
    elif arg == "async":
        asyncio.run(async_call())
    else:
        synchronous_call()
        asyncio.run(async_call())
