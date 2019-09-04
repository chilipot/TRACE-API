from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class Term(Base, Dictable):
    __tablename__ = 'term'

    exclude_dict_fields = ['categories']

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(200), nullable=False)

    categories = relationship('QuestionCategory', secondary='term_categories', back_populates='terms')

    @property
    def normal_title(self):
        return self.title.split(":").pop().strip().replace(' - ', ' ')
