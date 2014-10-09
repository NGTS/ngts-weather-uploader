#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paranal_query.query import *
from paranal_query.upload import upload_from_request, Measurement
import vcr
import datetime


def main():
    r = query_for_night(datetime.date(2014, 10, 7))
    data = parse_query_response(r.text)
    upload_from_request(r)


if __name__ == '__main__':
    main()
