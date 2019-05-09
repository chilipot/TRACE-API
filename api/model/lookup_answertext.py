from sqlalchemy import Column, Integer, Unicode

from api.model.mixins import Base, Dictable


class AnswerText(Base, Dictable):
    __tablename__ = 'lookup_answertext'

    id = Column(Integer, primary_key=True)
    text = Column(Unicode(500))
