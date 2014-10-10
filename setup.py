from setuptools import setup, find_packages

package_name = 'paranal_query'

setup(
    name=package_name,
    author='Simon Walker',
    author_email='s.r.walker101@googlemail.com',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'peewee',
        'python-dateutil',
        'pw-database-url',
    ],
    entry_points={
        'console_scripts': [
            'upload_paranal_metadata.py = {package_name}.__main__:main'.format(
                package_name=package_name),
        ],
    },
    package_data={
        package_name: ['logging_config.json'.format(package_name),]
    },
)
