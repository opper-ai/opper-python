import pytest
import time
from opperai import Client
from opperai.types.indexes import Document, Filter
from contextlib import contextmanager


@contextmanager
def index(name, _client: Client):
    idx = _client.indexes.create(name=name)
    try:
        yield idx
    finally:
        _client.indexes.delete(id=idx.id)


def test_create_index(vcr_cassette, client: Client):
    with index("test_create_index", client) as idx_id:
        assert idx_id is not None


def test_delete_index(client: Client, vcr_cassette):
    idx = client.indexes.create(name="test_delete_index")
    client.indexes.delete(id=idx.id)
    assert client.indexes.get(id=idx.id) is None


def test_get_by_id(vcr_cassette, client: Client):
    with index("test_get_by_id", client) as idx:
        idx_out = client.indexes.get(id=idx.id)
        assert idx_out.id == idx.id
        assert idx.name == "test_get_by_id"


def test_get_by_name(vcr_cassette, client: Client):
    with index("test_get_by_name", client) as idx:
        idx_out = client.indexes.get(name="test_get_by_name")
        assert idx_out.id == idx.id
        assert idx_out.name == "test_get_by_name"


def test_list_indexes(vcr_cassette, client: Client):
    idxs = client.indexes.list()
    assert len(idxs) == 0

    with index("test_list_indexes", client) as idx:
        idxs = client.indexes.list()
        assert len(idxs) == 1
        assert idxs[0].id == idx.id
        assert idxs[0].name == "test_list_indexes"

        with index("test_list_indexes_2", client) as idx_2:
            idxs = client.indexes.list()
            assert len(idxs) == 2
            assert idxs[1].id == idx_2.id
            assert idxs[1].name == "test_list_indexes_2"


def test_index_document(vcr_cassette, client: Client):
    with index("test_index_document", client) as idx:
        doc_in = Document(content="Hello", metadata={"source": "test"})
        doc_out = client.indexes.index(id=idx.id, doc=doc_in)
        assert doc_out.id is not None
        assert doc_out.uuid is not None
        assert doc_out.key is not None


def test_retrieve_document(vcr_cassette, client: Client):
    with index("test_retrieve_document", client) as idx:
        doc_in = Document(content="Hello", metadata={"source": "test"})
        client.indexes.index(id=idx.id, doc=doc_in)
        doc_retrieved = client.indexes.retrieve(id=idx.id, query="Hello", k=1)
        assert len(doc_retrieved) == 1
        assert doc_retrieved[0].content == "Hello"
        assert doc_retrieved[0].metadata == {"source": "test"}


@pytest.mark.skip(reason="Disabled due to pre signed urls")
def test_upload_file(client: Client, vcr_cassette):
    with index("test_upload_file", client) as idx:
        with open("/tmp/test.txt", "wb") as f:
            f.write(b"Hello")
            f.seek(0)
            client.indexes.upload_file(id=idx.id, file_path=f.name)
            time.sleep(0.5)  # wait for the file to be processed

        doc_retrieved = client.indexes.retrieve(id=idx.id, query="Hello", k=1)
        assert len(doc_retrieved) == 1
        assert doc_retrieved[0].content == "Hello"


def test_retrieve_filters(client: Client, vcr_cassette):
    with index("test_retrieve_filters", client) as idx:
        doc_in = Document(content="Bonjour", metadata={"source": "test"})
        client.indexes.index(id=idx.id, doc=doc_in)
        resp = client.indexes.retrieve(
            id=idx.id,
            query="test",
            k=1,
            filters=[Filter(key="source", operation="=", value="test")],
        )

        assert resp[0].content == "Bonjour"
        assert resp[0].metadata == {"source": "test"}
