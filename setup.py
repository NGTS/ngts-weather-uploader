from setuptools import setup, find_packages

setup(
    name='paranal_query',
    author='Simon Walker',
    author_email='s.r.walker101@googlemail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'peewee',
    ],
)
