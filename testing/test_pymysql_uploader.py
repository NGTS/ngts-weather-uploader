import pymysql
import pytest
import mock
from paranal_query.upload import PyMySQLUploader
from paranal_query.query import Query
import vcr
from contextlib import contextmanager


@contextmanager
def cassette():
    with vcr.use_cassette('testing/fixtures/ambient.yaml'):
        yield


@pytest.fixture
def connection():
    connection = PyMySQLUploader.connect()
    return connection


def test_it_creates_the_initial_table(connection):
    cursor = connection.cursor()
    cursor.execute('drop table if exists eso_paranal_ambient')
    cursor.execute('drop table if exists eso_paranal_weather')

    query = mock.Mock(query_type='ambient')
    uploader = PyMySQLUploader(query=query, request=None)

    cursor.execute('show tables')
    tables = {row[0] for row in cursor.fetchall()}
    assert 'eso_paranal_ambient' in tables and 'eso_paranal_weather' in tables

    cursor.execute('describe eso_paranal_ambient')
    rows = [row[:2] for row in cursor.fetchall()]
    assert rows == [
        ('id', 'int(11)'),
        ('airmass', 'float'),
        ('ra', 'float'),
        ('tau0', 'float'),
        ('night', 'datetime'),
        ('interval', 'int(11)'),
        ('theta0', 'float'),
        ('declination', 'float'),
        ('flux_rms', 'float'),
        ('seeing', 'float'),
    ]

    cursor.execute('describe eso_paranal_weather')
    rows = [row[:2] for row in cursor.fetchall()]
    assert rows == [
        ('id', 'int(11)'),
        ('air_pressure_2m', 'float'),
        ('particule_count_20m', 'float'),
        ('humidity_30m', 'float'),
        ('5u_particule_count_20m', 'float'),
        ('dewtemp_30m', 'float'),
        ('ambient_temp', 'float'),
        ('ground_temp', 'float'),
        ('wind_direction_30m', 'float'),
        ('wind_speed_10m', 'float'),
        ('wind_speed_w', 'float'),
        ('wind_speed_30m', 'float'),
        ('wind_speed_u', 'float'),
        ('wind_speed_v', 'float'),
        ('5u_particule_count_30m', 'float'),
        ('ambient_temp_30m', 'float'),
        ('night', 'datetime'),
        ('dewtemp_2m', 'float'),
        ('interval', 'int(11)'),
        ('humidity_2m', 'float'),
        ('wind_direction_10m', 'float'),
        ('pressure_sea_level', 'float'),
        ('particule_count_30m', 'float'),
    ]


def test_upload_ambient(connection):
    cursor = connection.cursor()
    cursor.execute('drop table if exists eso_paranal_ambient')

    with cassette():
        query = Query('ambient', uploader_class=PyMySQLUploader)
        query.upload('2013-01-01')

    cursor.execute('select * from eso_paranal_ambient')
    assert cursor.rowcount >= 1


def test_upload_weather(connection):
    cursor = connection.cursor()
    cursor.execute('drop table if exists eso_paranal_weather')

    with vcr.use_cassette('testing/fixtures/weather.yml'):
        query = Query('weather', uploader_class=PyMySQLUploader)
        query.upload('2013-01-01')

    cursor.execute('select * from eso_paranal_weather')
    assert cursor.rowcount >= 1
