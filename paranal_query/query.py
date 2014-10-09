import requests
import datetime
from io import StringIO
import csv
from collections import defaultdict

ROOT_URL = 'http://archive.eso.org/wdb/wdb/eso/meteo_paranal/query'

session = requests.Session()


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

    for field in fields:
        payload[field] = True

    return session.post(ROOT_URL, data=payload)


def clean_response(text):
    lines = text.split('\n')
    return '\n'.join([line for line in lines[1:]
                      if line])


def parse_query_response(response):
    cleaned_text = clean_response(response.text)
    buffer = StringIO(cleaned_text)
    reader = csv.DictReader(buffer)

    out = defaultdict(list)
    for row in reader:
        for key in row:
            out[key].append(row[key])

    return out
