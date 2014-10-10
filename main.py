#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paranal_query.query import Query
from paranal_query.upload import upload_from_request
import datetime


def main():
    for database in ['weather', 'ambient']:
        query = Query(database)
        r = query.for_night()
        upload_from_request(query, r)


if __name__ == '__main__':
    main()
