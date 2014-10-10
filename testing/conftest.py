import pytest
import os

@pytest.fixture(autouse=True, scope='session')
def set_database_url():
    os.environ['DATABASE_URL'] = 'sqlite:////tmp/test.db'
