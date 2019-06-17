from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class QuestionCategory(Base, Dictable):
    __tablename__ = 'question_category'

    exclude_dict_fields = ['terms', 'answers']

    id = Column(Integer, primary_key=True)
    text = Column(Unicode(250))

    answers = relationship('LookupAnswer', secondary='category_answers', back_populates='categories')
    terms = relationship('Term', secondary='term_categories', back_populates='categories')
    questions = relationship('LookupQuestion', back_populates='category')
