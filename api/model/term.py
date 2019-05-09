from sqlalchemy import Column, Integer, Unicode

from api.model.mixins import Base, Dictable


class Term(Base, Dictable):
    __tablename__ = 'term'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(200), nullable=False)

    @property
    def normal_title(self):
        return self.title.split(":").pop().strip().replace(' - ', ' ')
