#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paranal_query.query import Query
import datetime


def main():
    start_date = datetime.date(2012, 2, 3)
    end_date = datetime.date(2012, 2, 5)
    for database in ['weather', 'ambient']:
        query = Query(database).upload(start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    main()
