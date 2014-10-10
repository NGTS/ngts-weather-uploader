from functools import partial
import datetime


def clean_response(text):
    lines = text.split('\n')
    return '\n'.join([line for line in lines
                      if line.startswith('Night') or line.startswith('20')])


def to_datetime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def safe_cast(value, caster):
    try:
        return caster(value)
    except ValueError:
        return None

safe_float = partial(safe_cast, caster=float)
safe_int = partial(safe_cast, caster=int)
