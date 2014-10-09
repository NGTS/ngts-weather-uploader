from paranal_query.query import (query_for_night,
                                 parse_query_response)
import datetime
import pytest
import mock


@pytest.fixture(scope='session')
def query_response():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return query_for_night()


@pytest.fixture(scope='session')
def parsed(query_response):
    return parse_query_response(query_response)


def test_query_for_night_status(query_response):
    assert query_response.status_code == 200


def test_parse_response():
    r = mock.Mock()
    r.text = 'value\n10\n'
    assert parse_query_response(r)['value'] == ['10', ]
