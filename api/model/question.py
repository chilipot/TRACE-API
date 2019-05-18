from sqlalchemy import Float, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class Question(Base, Dictable):
    __tablename__ = 'question'

    exclude_dict_fields = ['score_data']

    id = Column(Integer, primary_key=True)
    data_id = Column(Integer, ForeignKey('score_data.id'), nullable=False)
    lookup_question_id = Column(Integer, ForeignKey('lookup_question.id'), nullable=False)
    response_count = Column(Integer, nullable=False)
    response_rate = Column(Float)
    mean = Column(Float)
    median = Column(Float)
    std_dev = Column(Float)

    score_data = relationship('ScoreData', back_populates="questions")
    lookup_question = relationship('LookupQuestion', lazy='joined')
    answers = relationship('Answer', back_populates='question', lazy='joined')
