import peewee
import pw_database_url as db_uri

database_proxy = peewee.Proxy()


class BaseModel(peewee.Model):

    class Meta(object):
        database = database_proxy


class Measurement(BaseModel):
    pass


database = peewee.SqliteDatabase('/tmp/test.db')
database_proxy.initialize(database)


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
    database.create_tables([Measurement], safe=True)

    data = query.parse_query_response(r.text)
    with database.transaction():
        for entry in data:
            try:
                Measurement.create(**entry)
            except peewee.IntegrityError:
                pass
