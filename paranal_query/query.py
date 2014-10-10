import requests
import datetime
import sys
if sys.version_info.major >= 3:
    from io import StringIO
else:
    from StringIO import StringIO
import csv
from .weather import (ROOT_URL,
                      COLUMN_NAME_MAP,
                      COLUMN_DATA_CASTERS,
                      safe_float,
                      PAYLOAD)


session = requests.Session()


def query_for_night(night=None):
    PAYLOAD['night'] = str(night if night is not None
                           else datetime.date.today()),

    return session.post(ROOT_URL, data=PAYLOAD)


def clean_response(text):
    lines = text.split('\n')
    return '\n'.join([line for line in lines
                      if line.startswith('Night') or line.startswith('20')])


def parse_query_response(response_text):
    cleaned_text = clean_response(response_text)
    reader = csv.DictReader(StringIO(cleaned_text))

    out = (row for row in reader)

    return cast_data_types(rename_columns(out))


def cast_row(row):
    out = {}
    for key in row:
        value = row[key]
        if key in COLUMN_DATA_CASTERS:
            casted_value = COLUMN_DATA_CASTERS[key](value)
        else:
            casted_value = safe_float(value)
        out[key] = casted_value
    return out


def cast_data_types(data):
    return map(cast_row, data)


def rename_columns(data):
    for row in data:
        yield {COLUMN_NAME_MAP[key]: row[key] for key in row}

if __name__ == '__main__':
    import vcr
    with vcr.use_cassette('testing/fixtures/night.yaml'):
        r = query_for_night()

    data = parse_query_response(r.text)
