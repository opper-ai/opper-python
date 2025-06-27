import asyncio
import os
from opperai import Opper
from pydantic import BaseModel


async def async_crud_function():
    opper = Opper(os.getenv("OPPER_API_KEY"))

    class MyInput(BaseModel):
        name: str

    function = await opper.functions.create_async(
        name="python-crud-function",  # Can't be duplicated
        instructions="greet the user",
        model="openai/gpt-4o",
        input_schema=MyInput.model_json_schema(),
    )

    # use function to stream response
    stream_response = await opper.functions.stream_async(
        function_id=function.id, input=MyInput(name="world")
    )
    async for event in stream_response.result:  # loop through the events
        if hasattr(event, "data") and hasattr(event.data, "delta") and event.data.delta:
            print(event.data.delta, end="", flush=True)

    class MyResponse(BaseModel):
        greeting: str

    # update function to have output type
    await opper.functions.update_async(
        function_id=function.id, output_schema=MyResponse.model_json_schema()
    )

    # call function
    res = await opper.functions.call_async(
        function_id=function.id, input=MyInput(name="world")
    )
    print(res.json_payload)

    # call function with examples
    res = await opper.functions.call_async(
        function_id=function.id,
        input=MyInput(name="world"),
        examples=[
            {
                "input": MyInput(name="world"),
                "output": MyResponse(greeting="Hello, world!"),
            },
            {
                "input": MyInput(name="nick"),
                "output": MyResponse(greeting="Hello, nick!"),
            },
        ],
    )
    print(res.json_payload)

    # enable exact match cache for function
    await opper.functions.update_async(
        function_id=function.id,
        instructions="greet the user in german",
        configuration={
            "cache.exact_match_enabled": True,  # NOTE: not available yet
            "cache.exact_match_cache_ttl": 300,
        },
    )

    # call with cache - not cached
    res = await opper.functions.call_async(
        function_id=function.id, input=MyInput(name="world")
    )
    assert not res.cached
    print(f"Not cached: {res.json_payload}")

    # call with cache - cached
    res = await opper.functions.call_async(
        function_id=function.id, input=MyInput(name="world")
    )
    # assert res.cached
    print(f"Cached: {res.json_payload}")

    print(f"Deleted: {await opper.functions.delete_async(function_id=function.id)}")


def sync_crud_function():
    opper = Opper(os.getenv("OPPER_API_KEY"))

    class MyInput(BaseModel):
        name: str

    # create the function
    function = opper.functions.create(
        name="python-sync-crud-function",  # Can't be duplicated
        instructions="greet the user",
        model="openai/gpt-4o",
        input_schema=MyInput.model_json_schema(),
    )

    # stream response
    stream_response = opper.functions.stream(
        function_id=function.id, input=MyInput(name="world")
    )
    for event in stream_response.result:  # loop through the events
        if hasattr(event, "data") and hasattr(event.data, "delta") and event.data.delta:
            print(event.data.delta, end="", flush=True)

    class MyResponse(BaseModel):
        greeting: str

    # update function to have output type
    opper.functions.update(
        function_id=function.id, output_schema=MyResponse.model_json_schema()
    )

    # call
    res = opper.functions.call(function_id=function.id, input=MyInput(name="world"))
    print(res.json_payload)

    # call with examples
    res = opper.functions.call(
        function_id=function.id,
        input=MyInput(name="world"),
        examples=[
            {
                "input": MyInput(name="world"),
                "output": MyResponse(greeting="Hello, world!"),
            },
            {
                "input": MyInput(name="nick"),
                "output": MyResponse(greeting="Hello, nick!"),
            },
        ],
    )
    print(res.json_payload)

    # enable exact match cache
    opper.functions.update(
        function_id=function.id,
        instructions="greet the user in german",
        configuration={
            "cache.exact_match_enabled": True,  # NOTE not available yet
            "cache.exact_match_cache_ttl": 300,
        },
    )

    # call with cache - not cached
    res = opper.functions.call(function_id=function.id, input=MyInput(name="world"))
    assert not res.cached
    print(f"Not cached: {res.json_payload}")

    # call with cache - cached
    res = opper.functions.call(function_id=function.id, input=MyInput(name="world"))
    # assert res.cached
    print(f"Cached: {res.json_payload}")
    print(f"Deleted: {opper.functions.delete(function_id=function.id)}")

    print("Listing functions:")
    print(opper.functions.list(limit=10))


async def run_async():
    await async_crud_function()


def run_sync():
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
