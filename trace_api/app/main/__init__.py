import logging

import paralleldots
from elasticsearch import Elasticsearch
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config.get(
        'ELASTICSEARCH_URL') else None
    paralleldots.set_api_key(app.config.get('PARALLEL_DOTS_API_KEY'))
    app.paralleldots = paralleldots
    db.init_app(app)
    flask_bcrypt.init_app(app)
    logging.basicConfig()
    if app.config.get('SHOW_QUERIES_DEBUG', False):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    return app
