from .common import safe_int, to_datetime

ROOT_URL = 'http://archive.eso.org/wdb/wdb/eso/ambient_paranal/query'

COLUMN_NAME_MAP = {
    'Night': 'night',
    'Measurement interval[s]': 'interval',
    'RA [deg]': 'ra',
    'DEC [deg]': 'declination',
    'DIMM Seeing ["]': 'seeing',
    'DIMM Airmass ["]': 'airmass',
    'Flux RMS': 'flux_rms',
    'Tau0 [ms]': 'tau0',
    'Theta0 ["]': 'theta0',
}

COLUMN_DATA_CASTERS = {
    'night': to_datetime,
    'interval': safe_int,
}

PAYLOAD = {
    'wdbo': 'csv/download',
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
