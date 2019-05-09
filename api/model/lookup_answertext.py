from sqlalchemy import Column, Integer, Unicode

from api import db
from api.model.mixins import Dictable


class AnswerText(db.Model, Dictable):
    __tablename__ = 'lookup_answertext'

    id = Column(Integer, primary_key=True)
    text = Column(Unicode(500))
