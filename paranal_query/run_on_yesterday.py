#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import datetime

from .query import Query
from .common import parse_date

class NullArgs(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return str(self.__dict__)


def main():
    args = parse_args()
    today = datetime.date.today()

    # Subtract two days to get the previous night
    yesterday = today - datetime.timedelta(days=1)
    start = datetime.datetime.combine(yesterday, datetime.time.min)
    end = datetime.datetime.combine(yesterday, datetime.time.max)

    query_args = NullArgs(
            night=None,
            start_date=str(start),
            end_date=str(end))
    Query.upload_from_args(query_args)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    main()
