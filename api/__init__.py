import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch

from api.config import config_by_name
from api.controller import api

db = SQLAlchemy()


def create_app(config_name):
    app = Flask('TRACE-API')
    app.config.from_object(config_by_name[config_name])
    app.elasticsearch = Elasticsearch(
        [app.config['ELASTICSEARCH_URL']]) if app.config.get(
        'ELASTICSEARCH_URL') else None
    db.init_app(app)
    app.register_blueprint(api)
    logging.basicConfig()
    if app.config.get('SHOW_QUERIES_DEBUG', False):
        logging.getLogger('sqlalchemy.engine').setLevel(app.config.get('LOG_LEVEL'))
    return app
