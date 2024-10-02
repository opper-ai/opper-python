import asyncio

from pydantic import BaseModel

from opperai import AsyncOpper, Opper
from opperai.types import Example


async def async_crud_function():
    opper = AsyncOpper()

    class MyInput(BaseModel):
        name: str

    class MyResponse(BaseModel):
        greeting: str

    function = await opper.functions.create(
        path="python/sdk/async-crud-function",
        instructions="greet the user",
        model="openai/gpt-4o",
        input_type=MyInput,
        output_type=MyResponse,
    )
    print(function)

    res, _ = await function.call(
        MyInput(name="world"),
        output_type=MyResponse,
        examples=[
            Example(
                input=MyInput(name="world"), output=MyResponse(greeting="Hello, world!")
            ),
            Example(
                input=MyInput(name="nick"), output=MyResponse(greeting="Hello, nick!")
            ),
        ],
    )
    print(res)

    res, _ = await function.call(MyInput(name="world"))
    print(res)

    await function.update(instructions="greet the user in german")

    res, _ = await function.call(MyInput(name="world"))
    print(res)

    print(await function.delete())


def sync_crud_function():
    opper = Opper()

    class MyInput(BaseModel):
        name: str

    class MyResponse(BaseModel):
        greeting: str

    function = opper.functions.create(
        path="python/sdk/sync-crud-function",
        instructions="greet the user",
        model="openai/gpt-4o",
        input_type=MyInput,
        output_type=MyResponse,
    )
    print(function)

    res, _ = function.call(
        MyInput(name="world"),
        output_type=MyResponse,
    )
    print(res)

    res, _ = function.call(MyInput(name="world"))
    print(res)

    function.update(instructions="greet the user in german")

    res, _ = function.call(MyInput(name="world"))
    print(res)

    print(function.delete())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "async":
            asyncio.run(async_crud_function())
        elif sys.argv[1] == "sync":
            sync_crud_function()
    else:
        asyncio.run(async_crud_function())
        sync_crud_function()
