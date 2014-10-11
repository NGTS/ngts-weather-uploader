import mock
from paranal_query.upload import upload_from_request

@mock.patch('paranal_query.upload.build_database')
@mock.patch('paranal_query.upload.AmbientMeasurement')
def test_max_rows_warning(_, __, caplog):
    query = mock.MagicMock()
    response = mock.MagicMock()

    query.query_type = 'ambient'
    query.max_rows = 2
    query.parse_query_response.return_value = iter([
        {'a': 10}
    ] * 100)

    upload_from_request(query, response)

    warning_log = [record for record in caplog.records()
                   if record.levelname == 'WARNING'][0]
    assert 'Not all rows uploaded' in str(warning_log)
