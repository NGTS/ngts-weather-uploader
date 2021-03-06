from paranal_query.query import Query
import pytest
import datetime
import vcr
from contextlib import contextmanager

@contextmanager
def cassette():
    with vcr.use_cassette('testing/fixtures/ambient.yaml'):
        yield


@pytest.fixture
def query_instance():
    return Query('ambient')


@pytest.fixture
def query_response(query_instance):
    d = datetime.date(2011, 3, 15)
    with cassette():
        return query_instance.for_night(d)


def test_construction(query_instance):
    assert isinstance(query_instance, Query)


def test_query_for_night_status(query_response):
    assert query_response.status_code == 200


def test_rename_columns(query_instance):

    data = [{
        'Tau0 [ms]': 1,
        'DIMM Seeing ["]': 2,
    }]

    assert list(query_instance.rename_columns(data)) == [{
        'tau0': 1,
        'seeing': 2,
    }]


def test_cast_data_types(query_instance):
    data = [{
        'night': '2014-10-09 12:00:33',
        'airmass': '1.2',
    }]

    assert list(query_instance.cast_data_types(data)) == [{
        'night': datetime.datetime(2014, 10, 9, 12, 0, 33),
        'airmass': 1.2,
    }]


def test_parse_response(monkeypatch, query_instance):
    monkeypatch.setattr(query_instance, 'rename_columns',
                        lambda value: value)
    response_text = 'Night,value\n2014,10'
    assert list(query_instance.parse_query_response(response_text))[0]['value'] == 10
