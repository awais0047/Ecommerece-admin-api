import os

from config import *


def compile_url(protocol='http', host='', port='', uri='', user='', password=''):
    credentials = user + f':{password}' if user and password else user
    location = host + f':{port}' if port else host
    url = f'{protocol}://{f"{credentials}@" if credentials else ""}{location}/'
    url = url + uri.lstrip('/') if uri else url

    return url


POSTGRESQL_DATABASE_URL = compile_url(
    protocol=POSTGRESQL_PROTOCOL,
    host=POSTGRESQL_HOST,
    port=POSTGRESQL_PORT,
    user=POSTGRESQL_USER,
    password=POSTGRESQL_PASSWORD,
    uri=POSTGRESQL_DATABASE_NAME
    )
