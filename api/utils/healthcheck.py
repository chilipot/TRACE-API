import os


def test_db() -> bool:
    """
    Establishes a connection to the database
    :return: True if the connection is established
    """
    try:
        from sqlalchemy import create_engine
        db_session = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
        db_session.connect()
        return True
    except Exception as e:
        print("Was unable to establish a connection to the database")
        print(e)
        return False


def test_es() -> bool:
    """
    Establishes a connection to the Elasticsearch instance
    :return: True if the connection is established
    """
    try:
        from elasticsearch import Elasticsearch
        elasticsearch = Elasticsearch([os.getenv('ELASTICSEARCH_URL')], verify_certs=True) if os.getenv(
            'ELASTICSEARCH_URL') else None
        elasticsearch.ping()
        return True
    except Exception as e:
        print("Was unable to establish a connection to elasticsearch")
        print(e)
        return False


def healthcheck():
    database = test_db()
    elasticsearch = test_es()
    return {'status': database and elasticsearch}
