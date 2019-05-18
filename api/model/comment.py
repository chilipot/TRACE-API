from sqlalchemy import Column, Integer, Unicode, ForeignKey

from api.model.mixins import Base, Dictable


class Comment(Base, Dictable):
    __tablename__ = 'comment'

    dict_collapse = True

    id = Column(Integer, primary_key=True)
    text = Column(Unicode)
    report_id = Column(Integer, ForeignKey('course.id'), nullable=False)
