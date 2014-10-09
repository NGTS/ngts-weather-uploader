from paranal_query.query import (query_for_night,
                                 parse_query_response)
import datetime
import pytest
import mock
import vcr


@pytest.fixture(scope='session')
def query_response():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    with vcr.use_cassette('testing/fixtures/night.yaml'):
        return query_for_night()


@pytest.fixture(scope='session')
def parsed(query_response):
    return parse_query_response(query_response)


def test_query_for_night_status(query_response):
    assert query_response.status_code == 200


@mock.patch('paranal_query.query.rename_columns',
            side_effect=lambda value: value)
def test_parse_response(mock_rename_columns):
    response_text = 'Night,value\n2014,10'
    assert parse_query_response(response_text)['value'] == ['10', ]


def test_clean_response():
    from paranal_query.query import clean_response
    text = 'foo\nNight\nbar\n2014\n'
    assert clean_response(text) == 'Night\n2014'


def test_rename_columns():
    from paranal_query.query import rename_columns

    data = {
        'Wind Speed Component U [m/s]': 1,
        'Dew Temperature at 2m [C]': 2,
    }

    assert rename_columns(data) == {
        'wind_speed_u': 1,
        'dewtemp_2m': 2,
    }
