import asyncio

from opperai import AsyncOpper, Opper
from pydantic import BaseModel

opper = Opper()


def bare_minimum():
    output, _ = opper.call(
        instructions="answer the following question",
        input="what are some uses of 42",
    )
    print(output)


def bare_minimum_with_model():
    output, _ = opper.call(
        instructions="answer the following question",
        input="what are some uses of 42",
        model="mistral/mistral-tiny-eu",
    )
    print(output)


def structured_input_output():
    class Number(BaseModel):
        x: int

    output, _ = opper.call(
        instructions="given a list of numbers return the largest",
        input=[Number(x=6), Number(x=7)],
        output_type=Number,
    )

    print(output)


def synchronous_call():
    print("running synchronous calls")
    bare_minimum()
    bare_minimum_with_model()
    structured_input_output()


synchronous_call()

aopper = AsyncOpper()


async def async_bare_minimum():
    output, _ = await aopper.call(
        instructions="answer the following question",
        input="what are some uses of 42",
    )
    print(output)


async def async_bare_minimum_with_model():
    output, _ = await aopper.call(
        instructions="answer the following question",
        input="what are some uses of 42",
        model="mistral/mistral-tiny-eu",
    )
    print(output)


async def async_structured_input_output():
    class Number(BaseModel):
        x: int

    output, _ = await aopper.call(
        instructions="given a list of numbers return the largest",
        input=[Number(x=6), Number(x=7)],
        output_type=Number,
    )

    print(output)


async def async_call():
    print("running asynchronous calls")
    await async_bare_minimum()
    await async_bare_minimum_with_model()
    await async_structured_input_output()


asyncio.run(async_call())
