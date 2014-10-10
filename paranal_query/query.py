import requests
import datetime
import sys
if sys.version_info.major >= 3:
    from io import StringIO
else:
    from StringIO import StringIO
import csv
from .common import clean_response


session = requests.Session()



class Query(object):

    def __init__(self, query_type):
        self.query_type = query_type
        self.upload_data()

    def upload_data(self):
        if self.query_type.lower() == 'weather':
            from .weather import (ROOT_URL,
                                  COLUMN_NAME_MAP,
                                  COLUMN_DATA_CASTERS,
                                  safe_float,
                                  PAYLOAD)
        elif self.query_type.lower() == 'ambient':
            from .ambient import (ROOT_URL,
                                  COLUMN_NAME_MAP,
                                  COLUMN_DATA_CASTERS,
                                  safe_float,
                                  PAYLOAD)

        else:
            raise RuntimeError("Unknown query type: {}, options are "
                               "[weather,ambient]".format(
                                   self.query_type))

        self.ROOT_URL = ROOT_URL
        self.COLUMN_NAME_MAP = COLUMN_NAME_MAP
        self.COLUMN_DATA_CASTERS = COLUMN_DATA_CASTERS
        self.safe_float = safe_float
        self.PAYLOAD = PAYLOAD

    def query_for_night(self, night=None):
        payload = self.PAYLOAD.copy()
        payload['night'] = str(night if night is not None
                               else datetime.date.today()),

        return session.post(self.ROOT_URL, data=payload)

    def cast_row(self, row):
        out = {}
        for key in row:
            value = row[key]
            if key in self.COLUMN_DATA_CASTERS:
                casted_value = self.COLUMN_DATA_CASTERS[key](value)
            else:
                casted_value = self.safe_float(value)
            out[key] = casted_value
        return out

    def cast_data_types(self, data):
        return map(self.cast_row, data)

    def rename_columns(self, data):
        for row in data:
            yield {self.COLUMN_NAME_MAP[key]: row[key] for key in row}

    def parse_query_response(self, response_text):
        cleaned_text = clean_response(response_text)
        reader = csv.DictReader(StringIO(cleaned_text))

        out = (row for row in reader)

        return self.cast_data_types(self.rename_columns(out))
