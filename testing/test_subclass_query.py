from paranal_query.query import WeatherQuery, AmbientQuery
from contextlib import contextmanager
import mock
import vcr
import datetime
import pytest


@contextmanager
def cassette(cassette_name):
    with vcr.use_cassette('testing/fixtures/{}.yaml'.format(cassette_name)):
        yield


@pytest.fixture
def chosen_date():
    return datetime.date(2013, 1, 1)


@mock.patch('paranal_query.query.PyMySQLUploader')
def test_weather_constructor(mock_uploader):
    w = WeatherQuery()

    with cassette('weather_query'):
        w.upload()


def test_weather_class_query_method(chosen_date):
    with cassette('weather_classmethod_query'):
        response = WeatherQuery.query_for_night(chosen_date)

    assert response.status_code == 200


@mock.patch('paranal_query.query.PyMySQLUploader')
def test_ambient_constructor(chosen_date):
    w = AmbientQuery()

    with cassette('ambient_query'):
        w.upload()


def test_ambient_class_query_method():
    with cassette('ambient_classmethod_query'):
        response = AmbientQuery.query_for_night(chosen_date)

    assert response.status_code == 200
