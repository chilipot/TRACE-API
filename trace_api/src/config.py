import os, codecs, logging
from cryptography.fernet import Fernet

basedir = os.path.abspath(os.path.dirname(__file__))
cipher_suite = Fernet(codecs.encode(os.getenv('CIPHER_KEY')))


def env_value(env, default=""):
    return cipher_suite.decrypt(os.getenv(env, default).encode('ascii')).decode(
        'ascii')
    # return os.getenv(env)


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
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SHOW_QUERIES_DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    LOG_LEVEL = logging.INFO


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
