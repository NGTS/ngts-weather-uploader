import pytest
import os

@pytest.fixture(autouse=True)
def set_database_url(tmpdir):
    path = tmpdir.join('test.db')
    os.environ['DATABASE_URL'] = 'sqlite://{}'.format(path)
