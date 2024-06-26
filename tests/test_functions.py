from contextlib import contextmanager

import pytest
from httpx import Response
from opperai import Client
from opperai.types import (
    CacheConfiguration,
    ChatPayload,
    Error,
    Errors,
    Function,
    Message,
    MessageContent,
)
from opperai.types.exceptions import StructuredGenerationError


@contextmanager
def _function(desc: Function, c: Client):
    function = c.functions.create(desc)
    yield function
    c.functions.delete(uuid=function.uuid)


def test_create_function(vcr_cassette, client: Client):
    with _function(
        Function(
            path="test/sdk/test_create_function",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as function:
        assert function is not None


def test_get_by_id(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_get_by_id",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as function:
        f_by_id = client.functions.get(uuid=function.uuid)
        assert f_by_id.path == "test/sdk/test_get_by_id"


def test_get_by_path(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_get_by_path",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as function:
        f_by_path = client.functions.get(path=function.path)
        assert f_by_path.path == "test/sdk/test_get_by_path"


def test_update_function(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_update_function",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        f.instructions = "Do something else"
        f1 = client.functions.update(f)
        f2 = client.functions.get(uuid=f1.uuid)
        assert f1 == f2
        assert f2.instructions == "Do something else"


def test_delete_function_by_id(client: Client, vcr_cassette):
    function = client.functions.create(
        Function(
            path="test/sdk/test_delete_function_by_id",
            description="Test function",
            instructions="Do something",
        )
    )
    assert function is not None
    client.functions.delete(uuid=function.uuid)
    f = client.functions.get(uuid=function.uuid)
    assert f is None


def test_delete_function_by_path(client: Client, vcr_cassette):
    function = client.functions.create(
        Function(
            path="test/sdk/test_delete_function_by_path",
            description="Test function",
            instructions="Do something",
        )
    )
    assert function is not None
    client.functions.delete(path=function.path)
    f = client.functions.get(path=function.path)
    assert f is None


def test_image_url(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_image",
            instructions="describe the image",
            model="openai/gpt4-turbo",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        resp = client.functions.chat(
            f.path,
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


def test_image_file(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_image",
            instructions="describe the image",
            model="openai/gpt4-turbo",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        resp = client.functions.chat(
            f.path,
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


def test_chat(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_chat",
            description="Translate to French",
            instructions="Translate to French",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        resp = client.functions.chat(
            f.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )

        assert "bonjour" in resp.message.lower()


def test_chat_stream(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_sync_chat_stream",
            description="Translate to French",
            instructions="Translate to French",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        gen = client.functions.chat(
            f.path,
            ChatPayload(messages=[Message(role="user", content="hello")]),
            stream=True,
        )

        resp = "".join([message.delta for message in gen if message.delta])

        assert "bonjour" in resp.lower()


def test_create_function_with_cache(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_create_function_with_cache",
            description="Test function",
            instructions="Do something",
            cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
        ),
        client,
    ) as function:
        res = client.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = client.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached


def test_create_function_with_cache_flush(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_create_function_with_cache_sync_flush",
            description="Test function",
            instructions="Do something",
            cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
        ),
        client,
    ) as function:
        res = client.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = client.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached

        client.functions.flush_cache(uuid=function.uuid)
        res = client.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached


def test_failed_structured_generation():
    client = Client()

    def mock_request(method, url, **kwargs):
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
        client.functions.chat(
            "fake-path",
            ChatPayload(messages=[Message(role="user", content="hello")]),
        )
