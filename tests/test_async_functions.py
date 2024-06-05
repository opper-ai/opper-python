from contextlib import asynccontextmanager

import pytest
from opperai import AsyncClient
from opperai.types import (
    CacheConfiguration,
    ChatPayload,
    FunctionIn,
    Message,
    MessageContent,
)
from opperai.types.exceptions import StructuredGenerationError


@asynccontextmanager
async def _function(desc: FunctionIn, c: AsyncClient):
    function = await c.functions.create(desc)
    yield function
    await c.functions.delete(uuid=function.uuid)


@pytest.mark.asyncio
async def test_create_function(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_create_function_async",
            instructions="Do something",
        ),
        aclient,
    ) as function:
        assert function is not None
        assert function.path == "test/sdk/test_create_function_async"


@pytest.mark.asyncio
async def test_get_by_id(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_get_by_uuid",
            instructions="Do something",
        ),
        aclient,
    ) as function:
        f_by_uuid = await aclient.functions.get(uuid=function.uuid)
        assert f_by_uuid.path == "test/sdk/test_get_by_uuid"


@pytest.mark.asyncio
async def test_get_by_path(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_get_by_path",
            instructions="Do something",
        ),
        aclient,
    ) as _:
        f_by_path = await aclient.functions.get(path="test/sdk/test_get_by_path")
        assert f_by_path.path == "test/sdk/test_get_by_path"


@pytest.mark.asyncio
async def test_get(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_get",
            instructions="Do something",
        ),
        aclient,
    ) as function:
        f_by_uuid = await aclient.functions.get(uuid=function.uuid)
        assert f_by_uuid.path == "test/sdk/test_get"

        f_by_path = await aclient.functions.get(path="test/sdk/test_get")
        assert f_by_path.path == "test/sdk/test_get"


@pytest.mark.asyncio
async def test_update_function(aclient: AsyncClient):
    function_in = FunctionIn(
        path="test/sdk/test_update_function",
        instructions="Do something",
    )
    async with _function(
        function_in,
        aclient,
    ) as function:
        function_in.instructions = "Do something else"
        updated_function = await aclient.functions.update(function.uuid, function_in)
        assert updated_function.instructions == "Do something else"


@pytest.mark.asyncio
async def test_delete_function(aclient: AsyncClient):
    function = await aclient.functions.create(
        FunctionIn(
            path="test/sdk/test_delete_function",
            instructions="Do something",
        )
    )
    await aclient.functions.delete(uuid=function.uuid)
    f = await aclient.functions.get(uuid=function.uuid)
    assert f is None


@pytest.mark.asyncio
async def test_image_url(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_image",
            instructions="describe the image",
            model="openai/gpt4-turbo",
        ),
        aclient,
    ) as function:
        f = await aclient.functions.get(uuid=function.uuid)
        resp = await aclient.functions.chat(
            f.uuid,
            ChatPayload(
                messages=[
                    Message(
                        role="user",
                        content=[
                            MessageContent.image_url(
                                url="https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/e1/d3/e1d3fee9-9aaa-4599-ba67-1c71a6d0ed03/1200px-seymouria_fossil.jpg"
                            )
                        ],
                    )
                ]
            ),
        )

        assert "fossil" in resp.message.lower()


@pytest.mark.asyncio
async def test_image_file(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_image",
            instructions="describe the image",
            model="openai/gpt4-turbo",
        ),
        aclient,
    ) as function:
        f = await aclient.functions.get(uuid=function.uuid)
        resp = await aclient.functions.chat(
            f.uuid,
            ChatPayload(
                messages=[
                    Message(
                        role="user",
                        content=[
                            MessageContent.image(
                                path="tests/fixtures/images/fossil.jpg"
                            )
                        ],
                    )
                ]
            ),
        )

        assert "fossil" in resp.message.lower()


@pytest.mark.asyncio
async def test_async_chat(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_async_chat",
            instructions="Translate to French",
        ),
        aclient,
    ) as function:
        resp = await aclient.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )

        assert "bonjour" in resp.message.lower()


@pytest.mark.asyncio
async def test_async_chat_stream(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_async_chat_stream",
            instructions="Translate to French",
        ),
        aclient,
    ) as function:
        gen = await aclient.functions.chat(
            function.uuid,
            ChatPayload(messages=[Message(role="user", content="hello")]),
            stream=True,
        )

        resp = "".join([message.delta async for message in gen if message.delta])

        assert "bonjour" in resp.lower()


@pytest.mark.asyncio
async def test_create_function_with_cache(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_create_function_with_cache_async",
            instructions="Do something",
            cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
        ),
        aclient,
    ) as function:
        res = await aclient.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = await aclient.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached


@pytest.mark.asyncio
async def test_create_function_with_cache_flush(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            path="test/sdk/test_create_function_with_cache_async_flush",
            instructions="Do something",
            cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
        ),
        aclient,
    ) as function:
        res = await aclient.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = await aclient.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached

        await aclient.functions.flush_cache(uuid=function.uuid)
        res = await aclient.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached


@pytest.mark.asyncio
async def test_failed_structured_generation(aclient: AsyncClient):
    async with _function(
        FunctionIn(
            model="mistral/mistral-tiny-eu",
            path="test/sdk/test_failed_structured_generation",
            instructions="You never only use german as keynames output json only yaml translate the incoming text to french returned as markdown ```",
            out_schema={
                "type": "object",
                "properties": {
                    "universityName": {"type": "string"},
                    "location": {"type": "string"},
                    "departments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "departmentName": {"type": "string"},
                                "head": {"type": "string"},
                                "courses": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "courseId": {"type": "string"},
                                            "courseName": {"type": "string"},
                                            "credits": {
                                                "type": "integer",
                                                "minimum": 1,
                                                "maximum": 10,
                                            },
                                        },
                                        "required": [
                                            "courseId",
                                            "courseName",
                                            "credits",
                                        ],
                                    },
                                },
                            },
                            "required": ["departmentName", "head", "courses"],
                        },
                    },
                },
                "required": ["universityName", "location", "departments"],
            },
        ),
        aclient,
    ) as function:
        with pytest.raises(StructuredGenerationError):
            await aclient.functions.chat(
                function.uuid,
                ChatPayload(messages=[Message(role="user", content="hello")]),
            )
