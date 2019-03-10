import codecs
import os
from datetime import timedelta

from cryptography.fernet import Fernet

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)


def env_value(env, default=""):
    cipher_suite = Fernet(codecs.encode(os.getenv('CIPHER_KEY')))
    return cipher_suite.decrypt(os.getenv(env, default).encode('ascii')).decode('ascii')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
    DB_USER = os.getenv('DB_USERNAME')
    DB_PASSWORD = env_value('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@SQL5007.site4now.net/' \
                                  f'DB_A3CB61_TRACE?' + 'driver=FreeTDS'
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    PARALLEL_DOTS_API_KEY = env_value('PARALLEL_DOTS_API_KEY')
    SHOW_QUERIES_DEBUG = False
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHOW_QUERIES_DEBUG = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
