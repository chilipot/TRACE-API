from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.model.mixins import Base, Dictable


class Answer(Base, Dictable):
    __tablename__ = 'answer'

    exclude_dict_fields = ['question']

    id = Column(Integer, primary_key=True)
    answer_text_id = Column(Integer, ForeignKey('lookup_answertext.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    value = Column(Integer, nullable=False)

    lookup_text = relationship('AnswerText', lazy='joined')
    question = relationship('Question', back_populates="answers")
