from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api import db
from api.model.mixins import Dictable


class ScoreData(db.Model, Dictable):
    __tablename__ = 'score_data'

    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('course.id'))
    enrollment = Column(Integer)
    responses = Column(Integer)
    declines = Column(Integer)

    course = relationship('Course', back_populates='score_data', uselist=False)
    questions = relationship('Question', back_populates='score_data')

    # Extra logic for special scores return
    def as_dict(self, include_pk=True):
        fields = super(ScoreData, self).as_dict(include_pk)
        fields['id'] = fields.get('course', {}).get('id')
        fields['comments'] = [comment.as_dict(include_pk=False) for comment in self.course.comments]
        return fields
