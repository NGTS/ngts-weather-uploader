from paranal_query.query import Query
import pytest

@pytest.fixture
def query_instance():
    return Query('ambient')

def test_construction(query_instance):
    assert isinstance(query_instance, Query)
