from paranal_query.query import query_for_night
import datetime
import pytest


@pytest.fixture(scope='session')
def query_response():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return query_for_night()



def test_query_for_night_status(query_response):
    assert query_response.status_code == 200

