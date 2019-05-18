from sqlalchemy import Column, Integer, Unicode

from api.model.mixins import Base, Dictable


class QuestionCategory(Base, Dictable):
    __tablename__ = 'question_category'

    id = Column(Integer, primary_key=True)
    text = Column(Unicode(250))
