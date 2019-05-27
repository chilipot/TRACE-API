import os

from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(20)

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))

db_session = scoped_session(sessionmaker(bind=engine))

elasticsearch = Elasticsearch([os.getenv('ELASTICSEARCH_URL')]) if os.getenv('ELASTICSEARCH_URL') else None
key = os.getenv('SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
