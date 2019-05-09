import logging
import os

from elasticsearch import Elasticsearch
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from api.config import config_by_name
from api.controller import api

app_config = config_by_name[os.getenv('APP_ENVIRONMENT')]

engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)

db_session = scoped_session(sessionmaker(bind=engine))

elasticsearch = Elasticsearch(
    [app_config.ELASTICSEARCH_URL]) if app_config.ELASTICSEARCH_URL else None


def create_app(config_name):
    app = Flask('TRACE-API')
    app.config.from_object(app_config)
    # app.elasticsearch = Elasticsearch(
    #     [app.config['ELASTICSEARCH_URL']]) if app.config.get(
    #     'ELASTICSEARCH_URL') else None
    # db.init_app(app)
    app.register_blueprint(api)
    logging.basicConfig()
    if app.config.get('SHOW_QUERIES_DEBUG', False):
        logging.getLogger('sqlalchemy.engine').setLevel(app.config.get('LOG_LEVEL'))
    return app
