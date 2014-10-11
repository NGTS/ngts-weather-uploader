import requests
import datetime
import sys
if sys.version_info.major >= 3:
    from io import StringIO
else:
    from StringIO import StringIO
import csv
from .common import clean_response, safe_float, parse_date
from .upload import Uploader
from .logger import logger


class Query(object):

    QUERY_TYPES = ['weather', 'ambient']

    def __init__(self, query_type):
        self.query_type = query_type
        self.upload_data()
        self.session = requests.Session()
        self.max_rows = 1000000

        logger.info('Constructing `%s` query', self.query_type)

    def upload_data(self):
        if self.query_type.lower() == 'weather':
            from .weather import (ROOT_URL,
                                  COLUMN_NAME_MAP,
                                  COLUMN_DATA_CASTERS,
                                  PAYLOAD)
        elif self.query_type.lower() == 'ambient':
            from .ambient import (ROOT_URL,
                                  COLUMN_NAME_MAP,
                                  COLUMN_DATA_CASTERS,
                                  PAYLOAD)

        if self.query_type.lower() not in ['weather', 'ambient']:
            raise RuntimeError("Unknown query type: {}, options are "
                               "[weather,ambient]".format(
                                   self.query_type))

        self.ROOT_URL = ROOT_URL
        self.COLUMN_NAME_MAP = COLUMN_NAME_MAP
        self.COLUMN_DATA_CASTERS = COLUMN_DATA_CASTERS
        self.PAYLOAD = PAYLOAD

    def for_night(self, night=None):
        night = night if night is not None else datetime.date.today()
        payload = self.PAYLOAD.copy()
        payload['night'] = str(night),
        payload['max_rows_returned'] = self.max_rows
        logger.info('Querying for %s', night)

        return self.send_request(payload)

    def for_date_range(self, start_date, end_date=None):
        end_date = end_date if end_date is not None else datetime.date.today()
        logger.info('Querying from %s to %s', start_date, end_date)
        payload = self.PAYLOAD.copy()
        payload['stime'] = str(start_date)
        payload['starttime'] = '00'
        payload['etime'] = str(end_date)
        payload['endtime'] = '24'
        return self.send_request(payload)

    def send_request(self, data):
        logger.debug('Sending web request to %s', self.ROOT_URL)
        return self.session.post(self.ROOT_URL, data=data)

    def cast_row(self, row):
        out = {}
        for key in row:
            value = row[key]
            if key in self.COLUMN_DATA_CASTERS:
                casted_value = self.COLUMN_DATA_CASTERS[key](value)
            else:
                casted_value = safe_float(value)
            out[key] = casted_value
        return out

    def cast_data_types(self, data):
        return map(self.cast_row, data)

    def rename_columns(self, data):
        for row in data:
            yield {self.COLUMN_NAME_MAP[key]: row[key] for key in row}

    def parse_query_response(self, response_text):
        logger.debug('Parsing response')
        cleaned_text = clean_response(response_text)
        reader = csv.DictReader(StringIO(cleaned_text))

        out = (row for row in reader)

        return self.cast_data_types(self.rename_columns(out))

    def upload(self, night=None, start_date=None, end_date=None):
        if start_date is not None:
            response = self.for_date_range(start_date, end_date)
        else:
            response = self.for_night(night)

        Uploader.upload_from_request(self, response)

        return self

    @classmethod
    def query_for_night(cls, query_type, night=None):
        self = cls(query_type)
        return self.for_night(night)

    @classmethod
    def upload_from_args(cls, args):
        for key in cls.QUERY_TYPES:
            cls(key).upload(
                night=parse_date(args.night),
                start_date=parse_date(args.start_date),
                end_date=parse_date(args.end_date)
            )
