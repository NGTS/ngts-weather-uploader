import pymysql
from .logger import logger
import paranal_query.weather as paranal_weather
import paranal_query.ambient as paranal_ambient
from collections import OrderedDict


class UploaderBase(object):

    @classmethod
    def upload_from_request(cls, query, request):
        return cls(query, request).upload()

    def __init__(self, query, request):
        self.query = query
        self.request = request

        self.build_database()


class PyMySQLUploader(UploaderBase):
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
            self.cursor.execute(query, entry)
            row_count += 1

        self.connection.commit()
