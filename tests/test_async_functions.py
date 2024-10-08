from contextlib import asynccontextmanager

import pytest
from httpx import Response
from opperai import AsyncClient
from opperai.types import (
    CacheConfiguration,
    ChatPayload,
    Error,
    Errors,
    Function,
    ImageInput,
    Message,
)
from opperai.types.exceptions import StructuredGenerationError


@asynccontextmanager
async def _function(desc: Function, c: AsyncClient):
    function = await c.functions.create(desc)
    yield function
    await c.functions.delete(uuid=function.uuid)


@pytest.mark.asyncio(scope="module")
async def test_create_function(vcr_cassette, aclient: AsyncClient):
    async with _function(
        Function(
            path="test/sdk/test_create_function_async",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as function:
        assert function is not None
        assert function.path == "test/sdk/test_create_function_async"


@pytest.mark.asyncio(scope="module")
async def test_get_by_id(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_get_by_id",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as function:
        f_by_id = await aclient.functions.get(uuid=function.uuid)
        assert f_by_id.path == "test/sdk/test_get_by_id"


@pytest.mark.asyncio(scope="module")
async def test_get_by_path(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_get_by_path",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as _:
        f_by_path = await aclient.functions.get(path="test/sdk/test_get_by_path")
        assert f_by_path.path == "test/sdk/test_get_by_path"


@pytest.mark.asyncio(scope="module")
async def test_get(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_get",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as function:
        f_by_id = await aclient.functions.get(uuid=function.uuid)
        assert f_by_id.path == "test/sdk/test_get"

        f_by_path = await aclient.functions.get(path="test/sdk/test_get")
        assert f_by_path.path == "test/sdk/test_get"


@pytest.mark.asyncio(scope="module")
async def test_update_function(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_update_function",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as function:
        function.instructions = "Do something else"
        updated_function = await aclient.functions.update(function)
        assert updated_function.instructions == "Do something else"


@pytest.mark.asyncio(scope="module")
async def test_delete_function(aclient: AsyncClient, vcr_cassette):
    function = await aclient.functions.create(
        Function(
            path="test/sdk/test_delete_function",
            description="Test function",
            instructions="Do something",
        )
    )
    await aclient.functions.delete(uuid=function.uuid)
    f = await aclient.functions.get(uuid=function.uuid)
    assert f is None


@pytest.mark.asyncio(scope="module")
async def test_image_file(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_image",
            instructions="describe the image",
            model="openai/gpt-4o",
        ),
        aclient,
    ) as function:
        f = await aclient.functions.get(uuid=function.uuid)
        resp = await aclient.functions.chat(
            f.path,
            ChatPayload(
                messages=[
                    Message(
                        role="user",
                        content=[
                            ImageInput.from_path("tests/fixtures/images/fossil.jpg")
                        ],
                    )
                ]
            ),
        )

        assert "fossil" in resp.message.lower()


@pytest.mark.asyncio(scope="module")
async def test_async_chat(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_async_chat",
            description="Translate to French",
            instructions="Translate to French",
        ),
        aclient,
    ) as function:
        resp = await aclient.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )

        assert "bonjour" in resp.message.lower()


@pytest.mark.asyncio(scope="module")
async def test_async_chat_stream(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_async_chat_stream",
            description="Translate to French",
            instructions="Translate to French",
        ),
        aclient,
    ) as function:
        gen = await aclient.functions.chat(
            function.path,
            ChatPayload(messages=[Message(role="user", content="hello")]),
            stream=True,
        )

        resp = "".join([message.delta async for message in gen if message.delta])

        assert "bonjour" in resp.lower()


@pytest.mark.asyncio(scope="module")
async def test_create_function_with_cache(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_create_function_with_cache_async",
            description="Test function",
            instructions="Do something",
            cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
        ),
        aclient,
    ) as function:
        res = await aclient.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = await aclient.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached


@pytest.mark.asyncio(scope="module")
async def test_create_function_with_cache_flush(aclient: AsyncClient, vcr_cassette):
    async with _function(
        Function(
            path="test/sdk/test_create_function_with_cache_async_flush",
            description="Test function",
            instructions="Do something",
            cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
        ),
        aclient,
    ) as function:
        res = await aclient.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = await aclient.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached

        await aclient.functions.flush_cache(uuid=function.uuid)
        res = await aclient.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached


@pytest.mark.asyncio(scope="module")
async def test_failed_structured_generation():
    client = AsyncClient()

    async def mock_request(method, url, **kwargs):
        error = Errors(
            errors=[
                Error(
                    type="StructuredGenerationError",
                    message="test structured generation exception",
                    detail="test structured generation exception",
                )
            ]
        )

        return Response(
            status_code=400,
            json=error.model_dump(),
        )

    client.http_client.session.request = mock_request
    with pytest.raises(StructuredGenerationError):
        await client.functions.chat(
            "fake-path",
            ChatPayload(messages=[Message(role="user", content="hello")]),
        )
