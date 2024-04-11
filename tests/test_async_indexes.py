import pytest
import asyncio
from opperai import AsyncClient
from opperai.types.indexes import Document, Filter
from contextlib import asynccontextmanager


@asynccontextmanager
async def _index(name, _client: AsyncClient):
    index = await _client.indexes.create(name=name)
    try:
        yield index
    finally:
        await _client.indexes.delete(id=index.id)


@pytest.mark.asyncio(scope="module")
async def test_create_index(aclient: AsyncClient, vcr_cassette):
    async with _index("test_create_index", aclient) as index:
        assert index is not None


@pytest.mark.asyncio(scope="module")
async def test_delete_index(aclient: AsyncClient, vcr_cassette):
    async with _index("test_delete_index", aclient) as index:
        await aclient.indexes.delete(id=index.id)
        assert await aclient.indexes.get(id=index.id) is None


@pytest.mark.asyncio(scope="module")
async def test_get_by_id(vcr_cassette, aclient: AsyncClient):
    async with _index("test_get_by_id", aclient) as index:
        idx_out = await aclient.indexes.get(id=index.id)
        assert idx_out.id == index.id
        assert idx_out.name == "test_get_by_id"


@pytest.mark.asyncio(scope="module")
async def test_get_by_name(vcr_cassette, aclient: AsyncClient):
    async with _index("test_get_by_name", aclient) as index:
        idx_out = await aclient.indexes.get(name="test_get_by_name")
        assert idx_out.id == index.id
        assert idx_out.name == "test_get_by_name"


@pytest.mark.asyncio(scope="module")
async def test_list_indexes(vcr_cassette, aclient: AsyncClient):
    idxs = await aclient.indexes.list()
    assert len(idxs) == 0

    async with _index("test_list_indexes", aclient) as index:
        idxs = await aclient.indexes.list()
        assert len(idxs) == 1
        assert idxs[0].id == index.id
        assert idxs[0].name == "test_list_indexes"

        async with _index("test_list_indexes_2", aclient) as index_2:
            idxs = await aclient.indexes.list()
            assert len(idxs) == 2
            assert idxs[1].id == index_2.id
            assert idxs[1].name == "test_list_indexes_2"


@pytest.mark.asyncio(scope="module")
async def test_index_document(vcr_cassette, aclient: AsyncClient):
    async with _index("test_index_document", aclient) as index:
        doc_in = Document(content="Hello", metadata={"source": "test"})
        doc_out = await aclient.indexes.index(id=index.id, doc=doc_in)
        assert doc_out.id is not None
        assert doc_out.uuid is not None
        assert doc_out.key is not None


@pytest.mark.asyncio(scope="module")
async def test_retrieve_document(vcr_cassette, aclient: AsyncClient):
    async with _index("test_retrieve_document", aclient) as index:
        doc_in = Document(content="Hello", metadata={"source": "test"})
        await aclient.indexes.index(id=index.id, doc=doc_in)
        doc_retrieved = await aclient.indexes.retrieve(id=index.id, query="Hello", k=1)
        assert len(doc_retrieved) == 1
        assert doc_retrieved[0].content == "Hello"
        assert doc_retrieved[0].metadata == {"source": "test"}


@pytest.mark.skip(reason="Disabled due to pre signed urls")
@pytest.mark.asyncio(scope="module")
async def test_upload_file(aclient: AsyncClient, vcr_cassette):
    async with _index("test_upload_file", aclient) as index:
        with open("/tmp/test.txt", "wb") as f:
            f.write(b"Hello")
            f.seek(0)
            await aclient.indexes.upload_file(id=index.id, file_path=f.name)
            await asyncio.sleep(0.5)  # wait for the file to be processed

        doc_retrieved = await aclient.indexes.retrieve(id=index.id, query="Hello", k=1)
        assert len(doc_retrieved) == 1
        assert doc_retrieved[0].content == "Hello"


@pytest.mark.asyncio(scope="module")
async def test_retrieve_filters(aclient: AsyncClient, vcr_cassette):
    async with _index("test_retrieve_filters", aclient) as index:
        doc_in = Document(content="Bonjour", metadata={"source": "test"})
        await aclient.indexes.index(id=index.id, doc=doc_in)
        resp = await aclient.indexes.retrieve(
            id=index.id,
            query="test",
            k=1,
            filters=[Filter(key="source", operation="=", value="test")],
        )

        assert resp[0].content == "Bonjour"
        assert resp[0].metadata == {"source": "test"}
