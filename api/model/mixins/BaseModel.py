from sqlalchemy.ext.declarative import declarative_base

from api import db_session

_Base = declarative_base()


class Base(_Base):
    __abstract__ = True
    query = db_session.query_property()
