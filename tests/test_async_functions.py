import pytest
from opperai import AsyncClient
from opperai.types import CacheConfiguration, ChatPayload, FunctionDescription, Message
from contextlib import asynccontextmanager


@asynccontextmanager
async def fn(desc: FunctionDescription, c: AsyncClient):
    fid = await c.functions.create(desc)
    yield fid
    await c.functions.delete(id=fid)


@pytest.mark.asyncio(scope="module")
async def test_create_function(vcr_cassette, aclient: AsyncClient):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_create_function_async",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as fid:
        assert fid is not None


@pytest.mark.asyncio(scope="module")
async def test_get_by_id(aclient: AsyncClient, vcr_cassette):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_get_by_id",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as fid:
        f_by_id = await aclient.functions.get_by_id(fid)
        assert f_by_id.path == "test/sdk/test_get_by_id"


@pytest.mark.asyncio(scope="module")
async def test_get_by_path(aclient: AsyncClient, vcr_cassette):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_get_by_path",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as _:
        f_by_path = await aclient.functions.get_by_path("test/sdk/test_get_by_path")
        assert f_by_path.path == "test/sdk/test_get_by_path"


@pytest.mark.asyncio(scope="module")
async def test_get(aclient: AsyncClient, vcr_cassette):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_get",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as fid:
        f_by_id = await aclient.functions.get(id=fid)
        assert f_by_id.path == "test/sdk/test_get"

        f_by_id = await aclient.functions.get(path="test/sdk/test_get")
        assert f_by_id.path == "test/sdk/test_get"


@pytest.mark.asyncio(scope="module")
async def test_update_function(aclient: AsyncClient, vcr_cassette):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_update_function",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as fid:
        f = await aclient.functions.get_by_id(fid)
        f.instructions = "Do something else"
        fn_id = await aclient.functions.update(f)
        f1 = await aclient.functions.get_by_id(fn_id)

    assert f1.instructions == "Do something else"


@pytest.mark.asyncio(scope="module")
async def test_delete_function_by_id(aclient: AsyncClient, vcr_cassette):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_delete_function_by_id",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as fid:
        f = await aclient.functions.get(id=fid)
        assert f is not None
        await aclient.functions.delete(id=f.id)
        f = await aclient.functions.get(id=f.id)
        assert f is None


@pytest.mark.asyncio(scope="module")
async def test_delete_function_by_path(aclient: AsyncClient, vcr_cassette):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_delete_function_by_path",
            description="Test function",
            instructions="Do something",
        ),
        aclient,
    ) as fid:
        f = await aclient.functions.get(id=fid)
        assert f is not None
        await aclient.functions.delete(path=f.path)
        f = await aclient.functions.get(path=f.path)
        assert f is None


@pytest.mark.asyncio(scope="module")
async def test_async_chat(aclient: AsyncClient, vcr_cassette):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_async_chat",
            description="Translate to French",
            instructions="Translate to French",
        ),
        aclient,
    ) as fid:
        f = await aclient.functions.get_by_id(fid)
        resp = await aclient.functions.chat(
            f.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )

        assert "bonjour" in resp.message.lower()


@pytest.mark.asyncio(scope="module")
async def test_async_chat_stream(aclient: AsyncClient, vcr_cassette):
    async with fn(
        FunctionDescription(
            path="test/sdk/test_async_chat_stream",
            description="Translate to French",
            instructions="Translate to French",
        ),
        aclient,
    ) as fid:
        f = await aclient.functions.get_by_id(fid)
        gen = await aclient.functions.chat(
            f.path,
            ChatPayload(messages=[Message(role="user", content="hello")]),
            stream=True,
        )

        resp = "".join([message.delta async for message in gen if message.delta])

        assert "bonjour" in resp.lower()


@pytest.mark.asyncio(scope="module")
async def test_create_function_with_cache(aclient: AsyncClient, vcr_cassette):
    fdesc = FunctionDescription(
        path="test/sdk/test_create_function_with_cache_async",
        description="Test function",
        instructions="Do something",
        cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
    )

    try:
        fid = await aclient.functions.create(fdesc)
        assert fid is not None

        res = await aclient.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = await aclient.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached
    finally:
        await aclient.functions.delete(path=fdesc.path)


@pytest.mark.asyncio(scope="module")
async def test_create_function_with_cache_flush(aclient: AsyncClient, vcr_cassette):
    fdesc = FunctionDescription(
        path="test/sdk/test_create_function_with_cache_async_flush",
        description="Test function",
        instructions="Do something",
        cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
    )
    try:
        fid = await aclient.functions.create(fdesc)
        assert fid is not None

        res = await aclient.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = await aclient.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached

        await aclient.functions.flush_cache(id=fid)
        res = await aclient.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached
    finally:
        await aclient.functions.delete(path=fdesc.path)
