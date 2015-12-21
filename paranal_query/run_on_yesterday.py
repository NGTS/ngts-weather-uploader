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

    # Subtract two days to get the previous night
    yesterday = today - datetime.timedelta(days=2)
    query_args = NullArgs(
        night=str(yesterday),
        start_date=None,
        end_date=None,
        db_host=args.db_host,
        db_user=args.db_user,
        db_name=args.db_name,
        verbose=args.verbose,
    )
    Query.upload_from_args(query_args)

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-H', '--db-host', required=False,
                        help='Database host', default='ngtsdb')
    parser.add_argument('-U', '--db-user', required=False,
                        help='Database host', default='sw')
    parser.add_argument('-D', '--db-name', required=False,
                        help='Database host', default='ngts_ops')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    main()
