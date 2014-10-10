#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paranal_query.query import Query
import datetime
import argparse


def main():
    args = parse_args()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--night', required=False)
    parser.add_argument('--start_date', required=False)
    parser.add_argument('--end_date', required=False)
    args = parser.parse_args()

    validate_args(args)
    return args



def validate_args(args):
    '''
    Ensure either:

        * no date arguments are given and assume todays date,
        * night and not start date or end date,
        * start date and not night or end_date
        * start_date and end_date and not night
    '''
    if ((not args.night and not args.start_date and not args.end_date) or
        (args.night and not args.start_date and not args.end_date) or
        (args.start_date and not args.night)):
        return
    else:
        raise RuntimeError("Invalid date combination passed")



if __name__ == '__main__':
    main()
