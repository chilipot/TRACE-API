from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class ScoreData(Base, Dictable):
    __tablename__ = 'score_data'

    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('course.id'))
    enrollment = Column(Integer)
    responses = Column(Integer)
    declines = Column(Integer)

    course = relationship('Course', back_populates='score_data', uselist=False)
    questions = relationship('Question', back_populates='score_data')
