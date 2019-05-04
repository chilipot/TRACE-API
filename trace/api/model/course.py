from sqlalchemy import Column, Integer, ForeignKey, Unicode
from sqlalchemy.orm import relationship

from api import db
from api.model.mixins import Dictable, CourseSearchable


class Course(db.Model, Dictable, CourseSearchable):
    __tablename__ = 'course'

    exclude_dict_fields = ['score_data', 'comments']

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    instructor_id = Column(Integer, ForeignKey('instructor.id'), nullable=False)
    term_id = Column(Integer, ForeignKey('term.id'), nullable=False)
    name = Column(Unicode(500), nullable=False)
    subject = Column(Unicode(50), nullable=False)
    number = Column(Integer, nullable=False)
    section = Column(Unicode(20))
    crn = Column(Unicode(20))

    instructor = relationship('Instructor', lazy='joined')
    term = relationship('Term', lazy='joined')
    department = relationship('Department', lazy='joined')
    score_data = relationship('ScoreData', back_populates='course', uselist=False)
    comments = relationship('Comment')

    @property
    def course_full_name(self):
        return f'{self.subject}{self.number} {self.name}'
