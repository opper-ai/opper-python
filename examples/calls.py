import asyncio

from opperai import AsyncOpper, Opper, trace
from pydantic import BaseModel

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


@trace
def synchronous_call():
    print("running synchronous calls")
    bare_minimum()
    bare_minimum_with_model()
    structured_input_output()


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


@trace
async def async_call():
    print("running asynchronous calls")
    await asyncio.gather(
        async_bare_minimum(),
        async_bare_minimum_with_model(),
        async_structured_input_output(),
    )


asyncio.run(async_call())
