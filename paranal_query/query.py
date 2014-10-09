import requests


class Query(object):
    ROOT_URL = 'http://archive.eso.org/wdb/wdb/eso/meteo_paranal/query'

    def __init__(self):
        self.night = None
        self.session = requests.Session()

    @classmethod
    def fetch_for_night(cls, night=None):
        return cls()
