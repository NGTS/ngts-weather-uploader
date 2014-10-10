from functools import partial
import datetime
from dateutil.parser import parse as dateutil_parse


def clean_response(text):
    lines = text.split('\n')
    return '\n'.join([line for line in lines
                      if line.startswith('Night') or line.startswith('20')])


def to_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def parse_date(s):
    return dateutil_parse(s).date()


def safe_cast(value, caster):
    try:
        return caster(value)
    except ValueError:
        return None

safe_float = partial(safe_cast, caster=float)
safe_int = partial(safe_cast, caster=int)
