import datetime

def test_parse_date():
    from paranal_query.common import parse_date
    for s in ['2014-02-15', '2014/2/15', '15/2/2014']:
        assert parse_date(s) == datetime.date(2014, 2, 15)
