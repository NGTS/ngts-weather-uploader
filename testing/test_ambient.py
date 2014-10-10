from paranal_query.query import Query
import pytest
import vcr

@pytest.fixture
def query_instance():
    return Query('ambient')

@pytest.fixture
def query_response(query_instance):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    with vcr.use_cassette('testing/fixtures/ambient.yaml'):
        return query_instance.query_for_night()


def test_construction(query_instance):
    assert isinstance(query_instance, Query)
