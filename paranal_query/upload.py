import peewee
import pw_database_url as db_uri
from .logger import logger
import paranal_query.weather as paranal_weather
import paranal_query.ambient as paranal_ambient

database_proxy = peewee.Proxy()


def build_database():
    config = db_uri.config()
    if 'sqlite' in config['engine'].lower():
        return build_sqlite_database(config)
    else:
        return build_mysql_database(config)


def build_sqlite_database(config):
    logger.debug('Connecting to sqlite database: %s', config['name'])
    from peewee import SqliteDatabase
    return SqliteDatabase(config['name'])


def build_mysql_database(config):
    logger.debug('Connecting to mysql database: %s', config['name'])
    from peewee import MySQLDatabase
    return MySQLDatabase(
        host=config['host'],
        database=config['name'],
        user=config['user'],
        port=config['port'] if config['port'] else 3306,
        password=config['password'],
    )

database_proxy = peewee.Proxy()


class BaseModel(peewee.Model):

    class Meta(object):
        database = database_proxy


class WeatherMeasurement(BaseModel):

    class Meta(object):
        db_table = 'paranal_weather'


class AmbientMeasurement(BaseModel):

    class Meta(object):
        db_table = 'paranal_ambient'


for column_name in paranal_weather.COLUMN_NAME_MAP.values():
    if column_name == 'night':
        column = peewee.DateTimeField(null=False, index=True, unique=True)
    elif column_name == 'interval':
        column = peewee.IntegerField()
    else:
        column = peewee.FloatField(null=True)

    column.add_to_class(WeatherMeasurement, column_name)


for column_name in paranal_ambient.COLUMN_NAME_MAP.values():
    if column_name == 'night':
        column = peewee.DateTimeField(null=False, index=True, unique=True)
    elif column_name == 'interval':
        column = peewee.IntegerField()
    else:
        column = peewee.FloatField(null=True)

    column.add_to_class(AmbientMeasurement, column_name)


def upload_from_request(query, r):
    logger.debug('Initialising database tables')

    database = build_database()
    database_proxy.initialize(database)
    database.create_tables([WeatherMeasurement, AmbientMeasurement], safe=True)

    if query.query_type.lower() == 'weather':
        model = WeatherMeasurement
    elif query.query_type.lower() == 'ambient':
        model = AmbientMeasurement

    data = query.parse_query_response(r.text)
    with database.transaction():
        for entry in data:
            try:
                model.create(**entry)
            except peewee.IntegrityError:
                pass
