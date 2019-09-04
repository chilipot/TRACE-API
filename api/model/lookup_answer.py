from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class LookupAnswer(Base, Dictable):
    __tablename__ = 'lookup_answer'

    exclude_dict_fields = ["categories"]

    # dict_collapse = True

    id = Column(Integer, primary_key=True)
    text = Column(Unicode(500))

    categories = relationship('QuestionCategory', secondary='category_answers', back_populates='answers')
