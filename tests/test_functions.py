from contextlib import contextmanager

import pytest
from opperai import Client
from opperai.types import (
    CacheConfiguration,
    ChatPayload,
    FunctionIn,
    Message,
    MessageContent,
)
from opperai.types.exceptions import StructuredGenerationError


@contextmanager
def _function(desc: FunctionIn, c: Client):
    function = c.functions.create(desc)
    yield function
    c.functions.delete(uuid=function.uuid)


def test_create_function(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_create_function",
            description="Test function",
            instructions="Do something",
        ),
        client,
    ) as function:
        assert function is not None


def test_get_by_uuid(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_get_by_uuid",
            instructions="Do something",
        ),
        client,
    ) as function:
        f_by_uuid = client.functions.get(uuid=function.uuid)
        assert f_by_uuid.path == "test/sdk/test_get_by_uuid"


def test_get_by_path(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_get_by_path",
            instructions="Do something",
        ),
        client,
    ) as function:
        f_by_path = client.functions.get(path=function.path)
        assert f_by_path.path == "test/sdk/test_get_by_path"


def test_update_function(client: Client):
    function_in = FunctionIn(
        path="test/sdk/test_update_function",
        instructions="Do something",
    )
    with _function(
        function_in,
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        function_in.instructions = "Do something else"
        f1 = client.functions.update(f.uuid, function_in)
        f2 = client.functions.get(uuid=f1.uuid)
        assert f1 == f2
        assert f2.instructions == "Do something else"


def test_delete_function_by_uuid(client: Client):
    function = client.functions.create(
        FunctionIn(
            path="test/sdk/test_delete_function_by_uuid",
            instructions="Do something",
        )
    )
    assert function is not None
    client.functions.delete(uuid=function.uuid)
    f = client.functions.get(uuid=function.uuid)
    assert f is None


def test_delete_function_by_path(client: Client):
    function = client.functions.create(
        FunctionIn(
            path="test/sdk/test_delete_function_by_path",
            instructions="Do something",
        )
    )
    assert function is not None
    client.functions.delete(path=function.path)
    f = client.functions.get(path=function.path)
    assert f is None


def test_image_url(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_image",
            instructions="describe the image",
            model="openai/gpt4-turbo",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        resp = client.functions.chat(
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


def test_image_file(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_image",
            instructions="describe the image",
            model="openai/gpt4-turbo",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        resp = client.functions.chat(
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


def test_chat(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_chat",
            instructions="Translate to French",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        resp = client.functions.chat(
            f.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )

        assert "bonjour" in resp.message.lower()


def test_chat_stream(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_sync_chat_stream",
            instructions="Translate to French",
        ),
        client,
    ) as function:
        f = client.functions.get(uuid=function.uuid)
        gen = client.functions.chat(
            f.uuid,
            ChatPayload(messages=[Message(role="user", content="hello")]),
            stream=True,
        )

        resp = "".join([message.delta for message in gen if message.delta])

        assert "bonjour" in resp.lower()


def test_create_function_with_cache(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_create_function_with_cache",
            instructions="Do something",
            cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
        ),
        client,
    ) as function:
        res = client.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = client.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached


def test_create_function_with_cache_flush(client: Client):
    with _function(
        FunctionIn(
            path="test/sdk/test_create_function_with_cache_sync_flush",
            instructions="Do something",
            cache_configuration=CacheConfiguration(exact_match_cache_ttl=10),
        ),
        client,
    ) as function:
        res = client.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached

        res = client.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert res.cached

        client.functions.flush_cache(uuid=function.uuid)
        res = client.functions.chat(
            function.uuid, ChatPayload(messages=[Message(role="user", content="hello")])
        )
        print(res)
        assert not res.cached


def test_failed_structured_generation(client: Client):
    with _function(
        FunctionIn(
            model="mistral/mistral-tiny-eu",
            path="test/sdk/test_failed_structured_generation",
            description="test structured generation exception",
            instructions="You never output json translate the incoming text to french returned as markdown ```",
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
                function.uuid,
                ChatPayload(messages=[Message(role="user", content="hello")]),
            )
