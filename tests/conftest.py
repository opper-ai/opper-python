import os
import re
import vcr
import pytest
from opperai import AsyncClient, Client


@pytest.fixture(scope="module")
def aclient() -> AsyncClient:
    yield AsyncClient()


@pytest.fixture(scope="module")
def client() -> Client:
    yield Client()


def uri_matcher(r1, r2):
    url_pattern = re.compile(r"https?://(api\.opper\.ai|localhost:8000)")
    uri1 = re.sub(url_pattern, "", r1.uri)
    uri2 = re.sub(url_pattern, "", r2.uri)

    return uri1 == uri2


@pytest.fixture
def vcr_cassette(request):
    test_name = request.node.name
    module_file = request.module.__file__
    file_name = os.path.splitext(os.path.basename(module_file))[0]

    cassette_name = f"{file_name}/{test_name}.yaml"

    my_vcr = vcr.VCR(
        cassette_library_dir="tests/fixtures/vcr_cassettes",
        path_transformer=vcr.VCR.ensure_suffix(".yaml"),
        filter_headers=[
            "x-opper-api-key",
            "host",
        ],
    )
    my_vcr.register_matcher("uri_matcher", uri_matcher)
    my_vcr.match_on = ["method", "body", "headers", "uri_matcher"]

    with my_vcr.use_cassette(cassette_name):
        yield
