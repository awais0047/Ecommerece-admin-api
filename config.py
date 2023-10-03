import os


conf = lambda x, y='': os.environ.get(x) or y

DEBUG = bool(int(conf('DEBUG', 0)))
LOG_LEVEL = conf('LOG_LEVEL', 'INFO')
APP_HOST = conf('APP_HOST', '0.0.0.0')
APP_PORT = int(conf('APP_PORT', '8000'))
URL_PREFIX = conf('URL_PREFIX')


POSTGRESQL_PROTOCOL = conf('POSTGRESQL_PROTOCOL', 'postgresql+psycopg2')
POSTGRESQL_HOST = conf('POSTGRESQL_HOST','localhost')
POSTGRESQL_PORT = conf('POSTGRESQL_PORT','5432')
POSTGRESQL_USER = conf('POSTGRESQL_USER','postgres')
POSTGRESQL_PASSWORD = conf('POSTGRESQL_PASSWORD','postgres')
POSTGRESQL_DATABASE_NAME = conf('POSTGRESQL_DATABASE_NAME','ecom1')
