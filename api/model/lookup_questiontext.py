from sqlalchemy import Integer, Column, Unicode

from api.model.mixins import Base, Dictable


class QuestionText(Base, Dictable):
    __tablename__ = 'lookup_questiontext'

    id = Column(Integer, primary_key=True)
    abbrev = Column(Unicode(250))
    text = Column(Unicode(500))
