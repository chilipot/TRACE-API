from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class Response(Base, Dictable):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    report_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    lookup_question_id = Column(Integer, ForeignKey('lookup_question.id'), nullable=False)
    lookup_answer_id = Column(Integer, ForeignKey('lookup_answer.id'), nullable=False)

    report = relationship('Course')
    lookup_question = relationship('LookupQuestion')
    lookup_answer = relationship('LookupAnswer')

    def __init__(self, user_id, report_id, lookup_question_id, lookup_answer_id):
        self.user_id = user_id
        self.report_id = report_id
        self.lookup_question_id = lookup_question_id
        self.lookup_answer_id = lookup_answer_id
