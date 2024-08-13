import asyncio
from typing import List

from opperai import AsyncOpper, Opper, trace
from opperai.types import Example
from pydantic import BaseModel, Field

opper = Opper()


def bare_minimum():
    output, _ = opper.call(
        name="python/sdk/bare-minimum",
        instructions="answer the following question",
        input="what are some uses of 42",
    )
    print(output)


def bare_minimum_with_model():
    output, _ = opper.call(
        name="python/sdk/bare-minimum-with-model",
        instructions="answer the following question",
        input="what are some uses of 42",
        model="mistral/mistral-tiny-eu",
    )
    print(output)


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


def call_with_structured_examples():
    class Number(BaseModel):
        x: int = Field(..., ge=0, description="value of the number")

    output, _ = opper.call(
        name="python/sdk/call-with-structured-pklexamples",
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
def synchronous_call():
    print("running synchronous calls")
    bare_minimum()
    bare_minimum_with_model()
    structured_input_output()
    call_with_structured_examples()
    call_with_examples()


synchronous_call()

aopper = AsyncOpper()


async def async_bare_minimum():
    output, _ = await aopper.call(
        name="python/sdk/async-bare-minimum",
        instructions="answer the following question",
        input="what are some uses of 42",
    )
    print(output)


async def async_bare_minimum_with_model():
    output, _ = await aopper.call(
        name="python/sdk/async-bare-minimum-with-model",
        instructions="answer the following question",
        input="what are some uses of 42",
        model="mistral/mistral-tiny-eu",
    )
    print(output)


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


async def async_call_with_examples():
    output, response = await aopper.call(
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
    )
    print(output)


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
async def async_call():
    print("running asynchronous calls")
    await asyncio.gather(
        async_bare_minimum(),
        async_bare_minimum_with_model(),
        async_structured_input_output(),
        async_call_with_examples(),
        async_call_with_structured_examples(),
    )


asyncio.run(async_call())
