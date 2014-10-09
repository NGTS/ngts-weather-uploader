#!/usr/bin/env python
# -*- coding: utf-8 -*-

from query import Query


def main():
    paranal_weather = Query.fetch_for_night()

if __name__ == '__main__':
    main()
