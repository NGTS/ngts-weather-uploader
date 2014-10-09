import requests
import datetime
from io import StringIO
import csv
from collections import defaultdict
from functools import partial

ROOT_URL = 'http://archive.eso.org/wdb/wdb/eso/meteo_paranal/query'

session = requests.Session()

COLUMN_NAME_MAP = {
    'Wind Speed Component U [m/s]': 'wind_speed_u',
    'Normalised Pressure at sea level [hPa]': 'pressure_sea_level',
    '0.5 micron Particule count at 30m [1/m^3]': 'particule_count_30m',
    'Wind Direction at 10m [deg]': 'wind_direction_10m',
    '0.5 micron Particule count at 20m [1/m^3]': 'particule_count_20m',
    'Wind Speed Component V [m/s]': 'wind_speed_v',
    'Ambient Temperature at 2m [C]': 'ambient_temp',
    'Wind Speed Component W [m/s]': 'wind_speed_w',
    'Night': 'night',
    'Wind Speed at 10m [m/s]': 'wind_speed_10m',
    'Measurement interval[s]': 'interval',
    'Relative Humidity at 30m [%]': 'humidity_30m',
    'Dew Temperature at 30m [C]': 'dewtemp_30m',
    'Dew Temperature at 2m [C]': 'dewtemp_2m',
    'Ground Temperature at -0.1m [C]': 'ground_temp',
    'Air Pressure at 2m [hPa]': 'air_pressure_2m',
    'Ambient Temperature at 30m [C]': 'ambient_temp_30m',
    'Relative Humidity at 2m [%]': 'humidity_2m',
    'Wind Direction at 30m [deg]': 'wind_direction_30m',
    '5.0 micron Particule count at 20m [1/m^3]': '5u_particule_count_20m',
    '5.0 micron Particule count at 30m [1/m^3]': '5u_particule_count_30m',
    'Wind Speed at 30m [m/s]': 'wind_speed_30m',
}


def to_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def safe_cast(value, caster):
    try:
        return caster(value)
    except ValueError:
        return None

safe_float = partial(safe_cast, caster=float)
safe_int = partial(safe_cast, caster=int)

COLUMN_DATA_CASTERS = {
    'night': to_datetime,
    'interval': safe_int,
}


def query_for_night(night=None):
    payload = {
        'night': night if night is not None else datetime.date.today(),
        'wdbo': 'csv/download',
        'max_rows_returned': 1000000,
    }

    fields = [
        'tab_interval', 'tab_t1', 'tab_t2', 'tab_t3', 'tab_td1',
        'tab_td2', 'tab_rh1', 'tab_rh2', 'tab_pr', 'tab_prq', 'tab_ws1',
        'tab_ws2', 'tab_wd1', 'tab_wd2', 'tab_wsu', 'tab_wsv', 'tab_wsw',
        'tab_dus1', 'tab_dul1', 'tab_dus2', 'tab_dul2',
    ]

    payload.update({field: True for field in fields})

    return session.post(ROOT_URL, data=payload)


def clean_response(text):
    lines = text.split('\n')
    return '\n'.join([line for line in lines
                      if line.startswith('Night') or line.startswith('20')])


def parse_query_response(response_text):
    cleaned_text = clean_response(response_text)
    buffer = StringIO(cleaned_text)
    reader = csv.DictReader(buffer)

    out = [row for row in reader]

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
    return list(map(cast_row, data))


def rename_columns(data):
    out = []
    for row in data:
        out.append({
            COLUMN_NAME_MAP[key]: row[key] for key in row
        })
    return out

if __name__ == '__main__':
    import vcr
    with vcr.use_cassette('testing/fixtures/night.yaml'):
        r = query_for_night()

    data = parse_query_response(r.text)
