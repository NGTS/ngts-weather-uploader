ngts-weather-uploader
=====================

[![Build Status](https://travis-ci.org/NGTS/ngts-weather-uploader.svg?branch=master)](https://travis-ci.org/NGTS/ngts-weather-uploader)
[![Code Health](https://landscape.io/github/NGTS/ngts-weather-uploader/master/landscape.png)](https://landscape.io/github/NGTS/ngts-weather-uploader/master)

For uploading ESO atomspheric information to the NGTS database. Data are uploaded for either a single night or date range to two databases:

* `eso_paranal_ambient`
* `eso_paranal_weather`

Installation
------------

The code is distributed as a python package, and so is installable through pip:

```
pip install git+https://github.com/NGTS/ngts-weather-uploader
```

The requirements are installed through the setup script. Alternatively install as a user:

```
git clone https://github.com/NGTS/ngts-weather-uploader
cd ngts-weather-uploader
python setup.py install --user

# or

pip install --user git+https://github.com/NGTS/ngts-weather-uploader
```

Running
-------

The database is specified on the command line, and assumed to be mysql.
See for example the command line usage for `run_on_yesterday.py`:


```sh
usage: run_on_yesterday.py [-h] [-H DB_HOST] [-U DB_USER] [-D DB_NAME]
[-v]

optional arguments:
  -h, --help            show this help message and exit
  -H DB_HOST, --db-host DB_HOST
                        Database host (default: ngtsdb)
  -U DB_USER, --db-user DB_USER
                        Database host (default: sw)
  -D DB_NAME, --db-name DB_NAME
                        Database host (default: ngts_ops)
  -v, --verbose
```
