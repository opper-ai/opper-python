import pytest
from opperai import Client
from opperai.types import CacheConfiguration, ChatPayload, FunctionDescription, Message
from contextlib import contextmanager


@contextmanager
def fn(desc: FunctionDescription, c: Client):
    fid = c.functions.create(desc)
    yield fid
    c.functions.delete(id=fid)


def test_create_function(vcr_cassette, client: Client):
    with fn(
        FunctionDescription(
            path="test/sdk/test_create_function",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as fid:
        assert fid is not None


def test_get_by_id(client: Client, vcr_cassette):
    with fn(
        FunctionDescription(
            path="test/sdk/test_get_by_id",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as fid:
        f_by_id = client.functions.get_by_id(fid)
        assert f_by_id.path == "test/sdk/test_get_by_id"


def test_get_by_path(client: Client, vcr_cassette):
    with fn(
        FunctionDescription(
            path="test/sdk/test_get_by_path",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as _:
        f_by_path = client.functions.get_by_path("test/sdk/test_get_by_path")
        assert f_by_path.path == "test/sdk/test_get_by_path"


def test_get(client: Client, vcr_cassette):
    with fn(
        FunctionDescription(
            path="test/sdk/test_get",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as fid:
        f_by_id = client.functions.get(id=fid)
        assert f_by_id.path == "test/sdk/test_get"

        f_by_id = client.functions.get(path="test/sdk/test_get")
        assert f_by_id.path == "test/sdk/test_get"


def test_update_function(client: Client, vcr_cassette):
    with fn(
        FunctionDescription(
            path="test/sdk/test_update_function",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as fid:
        f = client.functions.get_by_id(fid)
        f.instructions = "Do something else"
        fn_id = client.functions.update(f)
        f1 = client.functions.get_by_id(fn_id)

    assert f1.instructions == "Do something else"


def test_delete_function_by_id(client: Client, vcr_cassette):
    with fn(
        FunctionDescription(
            path="test/sdk/test_delete_function_by_id",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as fid:
        f = client.functions.get(id=fid)
        assert f is not None
        client.functions.delete(id=f.id)
        f = client.functions.get(id=f.id)
        assert f is None


def test_delete_function_by_path(client: Client, vcr_cassette):
    with fn(
        FunctionDescription(
            path="test/sdk/test_delete_function_by_path",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as fid:
        f = client.functions.get(id=fid)
        assert f is not None
        client.functions.delete(path=f.path)
        f = client.functions.get(path=f.path)
        assert f is None


def test_chat(client: Client, vcr_cassette):
    with fn(
        FunctionDescription(
            path="test/sdk/test_chat",
            description="Translate to French",
            instructions="Translate to French",
        ),
        client,
    ) as fid:
        f = client.functions.get_by_id(fid)
        resp = client.functions.chat(
            f.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )

        assert "bonjour" in resp.message.lower()


def test_chat_stream(client: Client, vcr_cassette):
    with fn(
        FunctionDescription(
            path="test/sdk/test_sync_chat_stream",
            description="Translate to French",
            instructions="Translate to French",
        ),
        client,
    ) as fid:
        f = client.functions.get_by_id(fid)
        gen = client.functions.chat(
            f.path,
            ChatPayload(messages=[Message(role="user", content="hello")]),
            stream=True,
        )

        resp = "".join([message.delta for message in gen if message.delta])

        assert "bonjour" in resp.lower()


def test_create_function_with_cache(client: Client, vcr_cassette):
    fdesc = FunctionDescription(
        path="test/sdk/test_create_function_with_cache_sync",
        description="Test function",
        instructions="Do something",
        cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
    )

    try:
        fid = client.functions.create(fdesc)
        assert fid is not None

        res = client.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = client.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached
    finally:
        client.functions.delete(path=fdesc.path)


def test_create_function_with_cache_flush(client: Client, vcr_cassette):
    fdesc = FunctionDescription(
        path="test/sdk/test_create_function_with_cache_sync_flush",
        description="Test function",
        instructions="Do something",
        cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
    )
    try:
        fid = client.functions.create(fdesc)
        assert fid is not None

        res = client.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = client.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached

        client.functions.flush_cache(id=fid)
        res = client.functions.chat(
            fdesc.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached
    finally:
        client.functions.delete(path=fdesc.path)
