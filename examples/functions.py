import asyncio

from pydantic import BaseModel

from opperai import AsyncOpper, Opper, fn
from opperai.types import Example, FunctionConfiguration, Message


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

    # call
    res, _ = await function.call(MyInput(name="world"))
    print(res)

    # call with examples
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

    # chat
    res = await function.chat(
        messages=[
            Message(role="user", content=MyInput(name="world").model_dump_json())
        ],
    )
    print(res)

    await function.update(
        instructions="greet the user in german",
        configuration=FunctionConfiguration(
            cache=FunctionConfiguration.Cache(
                exact_match_cache_ttl=10,
            ),
        ),
    )

    # call with cache - not cached
    res, response = await function.call(MyInput(name="world"))
    assert not response.cached
    print(f"Not cached: {res}")

    # call with cache - cached
    res, response = await function.call(MyInput(name="world"))
    assert response.cached
    print(f"Cached: {res}")

    print(f"Deleted: {await function.delete()}")


class TranslateOutput(BaseModel):
    german: str
    spanish: str
    french: str
    italian: str


@fn
async def async_translate(input: str) -> TranslateOutput:
    """Translate the input to multiple languages"""


@fn
def sync_translate(input: str) -> TranslateOutput:
    """Translate the input to multiple languages"""


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

    # call
    res, _ = function.call(MyInput(name="world"))
    print(res)

    # call with examples
    res, _ = function.call(
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

    # chat
    res = function.chat(
        messages=[
            Message(role="user", content=MyInput(name="world").model_dump_json())
        ],
    )
    print(res)

    function.update(
        instructions="greet the user in german",
        configuration=FunctionConfiguration(
            cache=FunctionConfiguration.Cache(
                exact_match_cache_ttl=10,
            ),
        ),
    )

    # call with cache - not cached
    res, response = function.call(MyInput(name="world"))
    assert not response.cached
    print(f"Not cached: {res}")

    # call with cache - cached
    res, response = function.call(MyInput(name="world"))
    assert response.cached
    print(f"Cached: {res}")

    print(f"Deleted: {function.delete()}")


async def run_async():
    print(await async_translate("hello"))
    await async_crud_function()


def run_sync():
    print(sync_translate("hello"))
    sync_crud_function()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "async":
            asyncio.run(run_async())
        elif sys.argv[1] == "sync":
            run_sync()
    else:
        asyncio.run(run_async())
        run_sync()
