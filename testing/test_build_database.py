from paranal_query.upload import build_database
import peewee
import os


def test_sqlite_construction():
    os.environ['DATABASE_URL'] = 'sqlite:////tmp/test.db'
    database = build_database()
    assert isinstance(database, peewee.SqliteDatabase)


def test_mysql_construction():
    os.environ['DATABASE_URL'] = 'mysql://sw@localhost/swdb'
    database = build_database()
    assert isinstance(database, peewee.MySQLDatabase)
