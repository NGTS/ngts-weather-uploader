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

The database to upload to is passed as the environment variable `DATABASE_URL` on the command line, in a format understandable to `peewee`, or `sqlalchemy`. For example:

```
DATABASE_URL=sqlite:///db.db upload_paranal_metadata.py --night 20150101

# or

DATABASE_URL=mysql://<user>@<host>/<dbname> upload_paranal_metadata.py --start-date 20150101 --end-date 20150201
```
