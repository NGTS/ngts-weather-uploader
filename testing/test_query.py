from paranal_query.query import Query
import datetime
import pytest
import vcr
from contextlib import contextmanager


@contextmanager
def cassette(cassette_name):
    with vcr.use_cassette('testing/fixtures/{}.yaml'.format(cassette_name)):
        yield


@pytest.fixture
def query_instance():
    return Query('weather')


@pytest.fixture
def query_response(query_instance):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    with cassette('weather_single_night'):
        return query_instance.for_night()


@pytest.fixture
def query_date_range(query_instance):
    start_date = datetime.date(2011, 3, 15)
    end_date = start_date + datetime.timedelta(days=2)

    with cassette('weather_date_range.yml'):
        response = query_instance.for_date_range(start_date, end_date)

    return response


def test_query_for_night_status(query_response):
    assert query_response.status_code == 200


def test_query_classmethod():
    with cassette('weather_single_night'):
        assert Query.query_for_night('weather').status_code == 200


def test_clean_response():
    from paranal_query.query import clean_response
    text = 'foo\nNight\nbar\n2014\n'
    assert clean_response(text) == 'Night\n2014'


def test_rename_columns(query_instance):

    data = [{
        'Wind Speed Component U [m/s]': 1,
        'Dew Temperature at 2m [C]': 2,
    }]

    assert list(query_instance.rename_columns(data)) == [{
        'wind_speed_u': 1,
        'dewtemp_2m': 2,
    }]


def test_cast_data_types(query_instance):
    data = [{
        'night': '2014-10-09 12:00:33',
        'humidity_2m': '0.3',
    }]

    assert list(query_instance.cast_data_types(data)) == [{
        'night': datetime.datetime(2014, 10, 9, 12, 0, 33),
        'humidity_2m': 0.3,
    }]


def test_parse_response(monkeypatch, query_instance):
    monkeypatch.setattr(query_instance, 'rename_columns',
                        lambda value: value)
    response_text = 'Night,value\n2014,10'
    value = list(query_instance.parse_query_response(response_text))[
        0]['value']
    assert value == 10


def test_date_range_response(query_date_range):
    assert query_date_range.status_code == 200


def test_date_range(query_instance, query_date_range):
    from itertools import islice
    parsed = query_instance.parse_query_response(query_date_range.text)
    parsed_list = list(parsed)
    first, last = parsed_list[0], parsed_list[-1]
    assert first['night'].date() == datetime.date(2011, 3, 15)
    assert last['night'].date() == datetime.date(2011, 3, 17)
