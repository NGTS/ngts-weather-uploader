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
    yesterday = today - datetime.timedelta(days=1)
    dt = datetime.datetime.combine(yesterday,
            datetime.datetime.min.time())
    query_args = NullArgs(
            night=str(yesterday),
            start_date=None,
            end_date=None)
    Query.upload_from_args(query_args)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    main()
