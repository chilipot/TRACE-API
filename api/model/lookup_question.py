from sqlalchemy import Integer, Column, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class LookupQuestion(Base, Dictable):
    __tablename__ = 'lookup_question'

    id = Column(Integer, primary_key=True)
    abbrev = Column(Unicode(250))
    text = Column(Unicode(500))
    category_id = Column(Integer, ForeignKey('question_category.id'), nullable=False)

    category = relationship('QuestionCategory', back_populates='questions', lazy='joined')
