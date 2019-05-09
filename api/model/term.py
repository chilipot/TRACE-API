from sqlalchemy import Column, Integer, Unicode

from api import db
from api.model.mixins import Dictable


class Term(db.Model, Dictable):
    __tablename__ = 'term'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(200), nullable=False)

    @property
    def normal_title(self):
        return self.title.split(":").pop().strip().replace(' - ', ' ')
