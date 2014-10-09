from peewee import *
from paranal_query.query import COLUMN_NAME_MAP, parse_query_response

database_proxy = Proxy()


class BaseModel(Model):

    class Meta:
        database = database_proxy


class Measurement(BaseModel):

    class Meta:
        db_table = 'paranal_weather'

column_count = 0
for column_name in COLUMN_NAME_MAP.values():
    if column_name == 'night':
        column = DateTimeField(null=False, index=True, unique=True)
    elif column_name == 'interval':
        column = IntegerField()
    else:
        column = FloatField(null=True)

    column.add_to_class(Measurement, column_name)
    column_count += 1

database = SqliteDatabase('/tmp/test.db')
database_proxy.initialize(database)

database.create_tables([Measurement], safe=True)


def upload_from_request(r):
    data = parse_query_response(r.text)
    for entry in data:
        try:
            Measurement.create(**entry)
        except IntegrityError:
            pass
