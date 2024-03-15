import vcr
import os
import re
import pytest
from opperai import AsyncClient
from opperai.types import ChatPayload, FunctionDescription, Message


DEFAULT_NAME = "test_function"
DEFAULT_DESCRIPTION = "Test function"
DEFAULT_INSTRUCTIONS = "Do something"


@pytest.fixture
async def function(
    request: pytest.FixtureRequest,
    client: AsyncClient,
):
    name = DEFAULT_NAME
    description = DEFAULT_DESCRIPTION
    instructions = DEFAULT_INSTRUCTIONS

    try:
        name = request.param.get("name", DEFAULT_NAME)
        description = request.param.get("description", DEFAULT_DESCRIPTION)
        instructions = request.param.get("instructions", DEFAULT_INSTRUCTIONS)
    except AttributeError:
        pass

    fdesc = FunctionDescription(
        path=f"test/sdk/{name}",
        description=description,
        instructions=instructions,
    )

    return await client.functions.create(fdesc)


@pytest.mark.asyncio(scope="module")
async def test_create_function(function, vcr_cassette):
    fid = await function
    assert fid is not None


@pytest.mark.parametrize("function", [{"name": "test_get_by_id"}], indirect=True)
@pytest.mark.asyncio(scope="module")
async def test_get_by_id(client: AsyncClient, function, vcr_cassette):
    fid = await function
    f_by_id = await client.functions.get_by_id(fid)
    assert f_by_id.path == "test/sdk/test_get_by_id"


@pytest.mark.parametrize("function", [{"name": "test_get_by_path"}], indirect=True)
@pytest.mark.asyncio(scope="module")
async def test_get_by_path(client: AsyncClient, function, vcr_cassette):
    await function
    f_by_path = await client.functions.get_by_path("test/sdk/test_get_by_path")
    assert f_by_path.path == "test/sdk/test_get_by_path"


@pytest.mark.parametrize("function", [{"name": "test_get"}], indirect=True)
@pytest.mark.asyncio(scope="module")
async def test_get(client: AsyncClient, function, vcr_cassette):
    fid = await function
    f_by_id = await client.functions.get(id=fid)
    assert f_by_id.path == "test/sdk/test_get"

    f_by_id = await client.functions.get(path="test/sdk/test_get")
    assert f_by_id.path == "test/sdk/test_get"


@pytest.mark.parametrize("function", [{"name": "test_update_function"}], indirect=True)
@pytest.mark.asyncio(scope="module")
async def test_update_function(client: AsyncClient, function, vcr_cassette):
    fid = await function
    f = await client.functions.get_by_id(fid)
    f.instructions = "Do something else"
    fn_id = await client.functions.update(f)
    f1 = await client.functions.get_by_id(fn_id)

    assert f1.instructions == "Do something else"


@pytest.mark.parametrize(
    "function", [{"name": "test_delete_function_by_id"}], indirect=True
)
@pytest.mark.asyncio(scope="module")
async def test_delete_function_by_id(client: AsyncClient, function, vcr_cassette):
    fid = await function
    f = await client.functions.get(id=fid)
    assert f is not None
    await client.functions.delete(id=f.id)
    f = await client.functions.get(id=f.id)
    assert f is None


@pytest.mark.parametrize(
    "function", [{"name": "test_delete_function_by_path"}], indirect=True
)
@pytest.mark.asyncio(scope="module")
async def test_delete_function_by_path(client: AsyncClient, function, vcr_cassette):
    fid = await function
    f = await client.functions.get(id=fid)
    assert f is not None
    await client.functions.delete(path=f.path)
    f = await client.functions.get(path=f.path)
    assert f is None


@pytest.mark.parametrize(
    "function",
    [{"name": "test_async_chat", "instructions": "translate to french"}],
    indirect=True,
)
@pytest.mark.asyncio(scope="module")
async def test_async_chat(function, client: AsyncClient, vcr_cassette):
    fid = await function
    f = await client.functions.get_by_id(fid)
    resp = await client.functions.chat(
        f.path, ChatPayload(messages=[Message(role="user", content="hello")])
    )

    assert resp.message == "Bonjour"


@pytest.mark.parametrize(
    "function",
    [{"name": "test_async_chat_stream", "instructions": "translate to french"}],
    indirect=True,
)
@pytest.mark.asyncio(scope="module")
async def test_async_chat_stream(function, client: AsyncClient, vcr_cassette):
    fid = await function
    f = await client.functions.get_by_id(fid)
    gen = await client.functions.chat(
        f.path,
        ChatPayload(messages=[Message(role="user", content="hello")]),
        stream=True,
    )

    resp = "".join([message.delta async for message in gen if message.delta])

    assert resp == "Bonjour"
