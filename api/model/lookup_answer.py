from sqlalchemy import Column, Integer, Unicode

from api.model.mixins import Base, Dictable


class LookupAnswer(Base, Dictable):
    __tablename__ = 'lookup_answer'

    dict_collapse = True

    id = Column(Integer, primary_key=True)
    text = Column(Unicode(500))
