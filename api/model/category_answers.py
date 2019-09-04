from sqlalchemy import Column, Integer, ForeignKey

from api.model.mixins import Base, Dictable


class CategoryAnswers(Base, Dictable):
    __tablename__ = 'category_answers'

    lookup_answer_id = Column(Integer, ForeignKey('lookup_answer.id'), primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey('question_category.id'), primary_key=True, nullable=False)
