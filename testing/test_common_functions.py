import datetime

def test_parse_date():
    from paranal_query.common import parse_date
    assert parse_date('2014-02-03') == datetime.date(2014, 2, 3)
