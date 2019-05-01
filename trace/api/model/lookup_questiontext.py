from sqlalchemy import Integer, Column, Unicode

from api import db
from api.model.mixins import Dictable


class QuestionText(db.Model, Dictable):
    __tablename__ = 'lookup_questiontext'

    id = Column(Integer, primary_key=True)
    abbrev = Column(Unicode(250))
    text = Column(Unicode(500))
