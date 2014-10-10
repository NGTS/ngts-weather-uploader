import peewee
import pw_database_url as db_uri

database_proxy = peewee.Proxy()


def build_database():
    config = db_uri.config()
    if 'sqlite' in config['engine'].lower():
        return build_sqlite_database(config)
    else:
        return build_mysql_database(config)


def build_sqlite_database(config):
    from peewee import SqliteDatabase
    return SqliteDatabase(config['name'])


def build_mysql_database(config):
    from peewee import MySQLDatabase
    return MySQLDatabase(
        host=config['host'],
        database=config['name'],
        user=config['user'],
        port=config['port'],
        password=config['password'],
    )

database_proxy = peewee.Proxy()


class Measurement(peewee.Model):

    class Meta(object):
        database = database_proxy


def upload_from_request(query, r):
    for column_name in query.COLUMN_NAME_MAP.values():
        if column_name == 'night':
            column = peewee.DateTimeField(null=False, index=True, unique=True)
        elif column_name == 'interval':
            column = peewee.IntegerField()
        else:
            column = peewee.FloatField(null=True)

        column.add_to_class(Measurement, column_name)

    Measurement._meta.db_table = 'paranal_{}'.format(query.query_type)
    database = build_database()
    database_proxy.initialize(database)
    database.create_tables([Measurement], safe=True)

    data = query.parse_query_response(r.text)
    with database.transaction():
        for entry in data:
            try:
                Measurement.create(**entry)
            except peewee.IntegrityError:
                pass
