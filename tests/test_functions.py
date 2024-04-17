from opperai import Client
from opperai.types import CacheConfiguration, ChatPayload, Function, Message
from contextlib import contextmanager
import pytest
from opperai.types.exceptions import StructuredGenerationError


@contextmanager
def _function(desc: Function, c: Client):
    function = c.functions.create(desc)
    yield function
    c.functions.delete(id=function.id)


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
        f_by_id = client.functions.get(id=function.id)
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
        f = client.functions.get(id=function.id)
        f.instructions = "Do something else"
        f1 = client.functions.update(f)
        f2 = client.functions.get(id=f1.id)
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
    client.functions.delete(id=function.id)
    f = client.functions.get(id=function.id)
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


def test_chat(client: Client, vcr_cassette):
    with _function(
        Function(
            path="test/sdk/test_chat",
            description="Translate to French",
            instructions="Translate to French",
        ),
        client,
    ) as function:
        f = client.functions.get(id=function.id)
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
        f = client.functions.get(id=function.id)
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

        client.functions.flush_cache(id=function.id)
        res = client.functions.chat(
            function.path, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached


def test_failed_structured_generation(client: Client, vcr_cassette):
    with _function(
        Function(
            model="mistral/mistral-tiny-eu",
            path="test/sdk/test_failed_structured_generation",
            description="test structured generation exception",
            instructions="You translate the incoming text to french",
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
        client,
    ) as function:
        with pytest.raises(StructuredGenerationError):
            client.functions.chat(
                function.path,
                ChatPayload(messages=[Message(role="user", content="hello")]),
            )
