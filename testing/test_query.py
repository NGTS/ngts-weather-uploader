from paranal_query.query import Query

def test_query_class_constructor():
    query = Query.fetch_for_night()
    assert isinstance(query, Query)
