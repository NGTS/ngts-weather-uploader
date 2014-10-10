from peewee import (
    DateTimeField,
    FloatField,
    IntegerField,
    IntegrityError,
    Model,
    Proxy,
    SqliteDatabase,
)

database_proxy = Proxy()


class BaseModel(Model):

    class Meta(object):
        database = database_proxy


class Measurement(BaseModel):
    pass


database = SqliteDatabase('/tmp/test.db')
database_proxy.initialize(database)


def upload_from_request(query, r):
    for column_name in query.COLUMN_NAME_MAP.values():
        if column_name == 'night':
            column = DateTimeField(null=False, index=True, unique=True)
        elif column_name == 'interval':
            column = IntegerField()
        else:
            column = FloatField(null=True)

        column.add_to_class(Measurement, column_name)

    Measurement._meta.db_table = 'paranal_{}'.format(query.query_type)
    database.create_tables([Measurement], safe=True)

    data = query.parse_query_response(r.text)
    for entry in data:
        try:
            Measurement.create(**entry)
        except IntegrityError:
            pass
