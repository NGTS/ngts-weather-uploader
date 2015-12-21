import peewee
import pw_database_url as db_uri
import pymysql
from .logger import logger
import paranal_query.weather as paranal_weather
import paranal_query.ambient as paranal_ambient
from collections import OrderedDict

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


class BaseModel(peewee.Model):

    class Meta(object):
        database = database_proxy


class WeatherMeasurement(BaseModel):

    class Meta(object):
        db_table = 'eso_paranal_weather'


class AmbientMeasurement(BaseModel):

    class Meta(object):
        db_table = 'eso_paranal_ambient'


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


class Uploader(object):

    @classmethod
    def upload_from_request(cls, query, request):
        return cls(query, request).upload()

    def __init__(self, query, request):
        self.query = query
        self.request = request

        self.build_database()

    def build_database(self):
        logger.debug('Initialising database tables')
        self.database = build_database()
        database_proxy.initialize(self.database)
        self.database.create_tables(
            [WeatherMeasurement, AmbientMeasurement], safe=True)

        if self.query.query_type.lower() == 'weather':
            self.model = WeatherMeasurement
        elif self.query.query_type.lower() == 'ambient':
            self.model = AmbientMeasurement

    def upload(self):
        data = self.query.parse_query_response(self.request.text)
        logger.info('Uploading data to database')
        with self.database.transaction():
            row_count = 0
            for entry in data:
                try:
                    self.model.create(**entry)
                except peewee.IntegrityError:
                    pass
                finally:
                    row_count += 1

            if row_count >= self.query.max_rows:
                logger.warning('Not all rows uploaded, consider querying for a '
                               'smaller date range or raising `query.max_rows`')


class PyMySQLUploader(Uploader):
    DB_HOST = 'localhost'
    DB_USER = 'simon'
    DB_DBNAME = 'test'

    AMBIENT_COLUMNS = OrderedDict([
        ('id', 'integer primary key auto_increment'),
        ('airmass', 'float'),
        ('ra', 'float'),
        ('tau0', 'float'),
        ('night', 'datetime'),
        ('interval', 'integer'),
        ('theta0', 'float'),
        ('declination', 'float'),
        ('flux_rms', 'float'),
        ('seeing', 'float'),
    ])

    WEATHER_COLUMNS = OrderedDict([
        ('id', 'integer primary key auto_increment'),
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
        ('interval', 'integer'),
        ('humidity_2m', 'float'),
        ('wind_direction_10m', 'float'),
        ('pressure_sea_level', 'float'),
        ('particule_count_30m', 'float'),
    ])

    COLUMN_NAME_MAP = {'eso_paranal_ambient': AMBIENT_COLUMNS,
                       'eso_paranal_weather': WEATHER_COLUMNS}

    def __init__(self, query, request):
        self.connection = self.connect()
        self.cursor = self.connection.cursor()
        super(PyMySQLUploader, self).__init__(query, request)

    @classmethod
    def connect(cls):
        return pymysql.connect(host=cls.DB_HOST, user=cls.DB_USER,
                               db=cls.DB_DBNAME)

    def construct_single_table(self, key):
        column_descriptions = []
        for (name, type) in self.COLUMN_NAME_MAP[key].items():
            row = '`{name}` {type}'.format(name=name, type=type)
            column_descriptions.append(row)
        self.cursor.execute('''create table if not exists {key} (
            {columns}
        )'''.format(key=key, columns=','.join(column_descriptions)))

    def build_database(self):
        logger.debug('Initialising database tables')
        for key in self.COLUMN_NAME_MAP.keys():
            self.construct_single_table(key)

        query_type = self.query.query_type.lower()
        if query_type == 'ambient':
            self.upload_table_name = 'eso_paranal_ambient'
        elif query_type == 'weather':
            self.upload_table_name = 'eso_paranal_weather'

    def upload(self):
        data = self.query.parse_query_response(self.request.text)
        logger.info('Uploading data to database')
        key_list = self.COLUMN_NAME_MAP[self.upload_table_name]
        keys = [colname for colname in key_list.keys()
                if colname != 'id']
        colnames = ','.join(['`{}`'.format(key) for key in keys])
        placeholders = ','.join(['%({name})s'.format(name=name)
                                 for name in keys])
        row_count = 0
        for entry in data:
            query = '''
            insert into {tablename} ({colnames}) values
            ({placeholders})'''.format(tablename=self.upload_table_name,
                                       colnames=colnames, placeholders=placeholders)
            print(query)
            self.cursor.execute(query, entry)
            row_count += 1

        self.connection.commit()
