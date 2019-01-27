
import os
basedir = os.path.abspath(os.path.dirname(__file__))

ENV_DB = 'sqlite:///catalog.db'
ENV_SKEY = 'BEANCOUNTER_SECRET_KEY'
ENV_BIND_IP = "127.0.0.1"
ENV_BIND_PORT = 5000

try:
    SQLALCHEMY_DATABASE_URI = os.environ[ENV_DB]
except KeyError:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bean_counter.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

try:
    SECRET_KEY = os.environ[ENV_SKEY]
except KeyError:
    SECRET_KEY = 'qwertyuiop[]'

try:
    BIND_IP = os.environ[ENV_BIND_IP]
    BIND_PORT = int(os.environ[ENV_BIND_PORT])
except KeyError:
    BIND_IP = '127.0.0.1'
    BIND_PORT = 5000
