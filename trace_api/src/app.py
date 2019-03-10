import redis
from src.controller import blueprint
from src.config import config_by_name
from elasticsearch import Elasticsearch
from flask import Flask
from src.model import db


def create_app():
    flask_app = Flask('TRACE')
    return flask_app


def configure_app(flask_app: Flask, config_name: str) -> Flask:
    flask_app.config.from_object(config_by_name[config_name])
    flask_app.elasticsearch = Elasticsearch(
        [flask_app.config['ELASTICSEARCH_URL']]) if flask_app.config.get(
        'ELASTICSEARCH_URL') else None
    flask_app.redis_pool = redis.ConnectionPool(host='redis', port=6379, db=0)
    db.init_app(flask_app)
    flask_app.register_blueprint(blueprint)
    flask_app.logger.info("Flask application created.")
    return flask_app


app_inst = create_app()
app = configure_app(app_inst, 'dev')
