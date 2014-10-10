#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paranal_query.query import Query
import datetime


def main():
    for database in ['weather', 'ambient']:
        query = Query(database)
        query.upload()


if __name__ == '__main__':
    main()
