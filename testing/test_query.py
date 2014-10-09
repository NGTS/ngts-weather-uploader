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
    response_text = 'Night,value\n2014,10'
    assert parse_query_response(response_text)['value'] == ['10', ]


def test_clean_response():
    from paranal_query.query import clean_response
    text = 'foo\nNight\nbar\n2014\n'
    assert clean_response(text) == 'Night\n2014'
