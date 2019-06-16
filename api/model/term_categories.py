from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class TermCategories(Base, Dictable):
    __tablename__ = 'term_categories'

    term_id = Column(Integer, ForeignKey('term.id'), primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey('question_category.id'), primary_key=True, nullable=False)