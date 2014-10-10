from functools import partial
import datetime


def to_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def safe_cast(value, caster):
    try:
        return caster(value)
    except ValueError:
        return None

safe_float = partial(safe_cast, caster=float)
safe_int = partial(safe_cast, caster=int)

ROOT_URL = 'http://archive.eso.org/wdb/wdb/eso/meteo_paranal/query'

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

COLUMN_DATA_CASTERS = {
    'night': to_datetime,
    'interval': safe_int,
}

PAYLOAD = {
    'wdbo': 'csv/download',
    'max_rows_returned': 1000000,
}

fields = [
    'tab_interval', 'tab_t1', 'tab_t2', 'tab_t3', 'tab_td1',
    'tab_td2', 'tab_rh1', 'tab_rh2', 'tab_pr', 'tab_prq', 'tab_ws1',
    'tab_ws2', 'tab_wd1', 'tab_wd2', 'tab_wsu', 'tab_wsv', 'tab_wsw',
    'tab_dus1', 'tab_dul1', 'tab_dus2', 'tab_dul2',
]

PAYLOAD.update({field: True for field in fields})
