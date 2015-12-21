import vcr
import pytest
import pymysql

from paranal_query.upload import PyMySQLUploader
from paranal_query.query import Query


@pytest.yield_fixture(scope='session')
def connection():
    PyMySQLUploader.DB_HOST = 'localhost'
    PyMySQLUploader.DB_USER = 'simon'
    PyMySQLUploader.DB_DBNAME = 'test'

    connection = pymysql.connect(
        host=PyMySQLUploader.DB_HOST,
        user=PyMySQLUploader.DB_USER,
        db=PyMySQLUploader.DB_DBNAME)

    yield connection
    connection.close()


def get_nrows(cursor, table):
    cursor.execute('select count(*) from {table}'.format(table=table))
    return cursor.fetchone()[0]


@vcr.use_cassette('testing/fixtures/ambient_no_duplicates.yaml')
def test_no_duplicates(connection):
    cursor = connection.cursor()
    cursor.execute('drop table if exists eso_paranal_ambient')

    query = Query('ambient')
    response = query.for_night('2015-01-01')
    uploader = PyMySQLUploader(query, response)
    assert get_nrows(cursor, 'eso_paranal_ambient') == 0

    uploader.upload()

    initial_nrows = get_nrows(uploader.connection.cursor(), 'eso_paranal_ambient')
    assert initial_nrows == 386

    uploader.upload()
    new_nrows = get_nrows(uploader.connection.cursor(), 'eso_paranal_ambient')
    assert new_nrows == 386
    uploader.connection.close()
