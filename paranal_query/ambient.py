from .common import safe_int, to_datetime

ROOT_URL = 'http://archive.eso.org/wdb/wdb/eso/ambient_paranal/query'

COLUMN_NAME_MAP = {
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
'tab_interval',
'tab_ra',
'tab_dec',
'tab_fwhm',
'tab_airmass',
'tab_rfl',
'tab_tau',
'tab_tet',
]

PAYLOAD.update({field: True for field in fields})

